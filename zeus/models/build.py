from sqlalchemy import event
from sqlalchemy.sql import func, select

from zeus.config import db
from zeus.constants import Status, Result
from zeus.db.mixins import RepositoryBoundMixin, StandardAttributes
from zeus.db.types import Enum, GUID, JSONEncodedDict
from zeus.db.utils import model_repr
from zeus.utils import timezone

build_author_table = db.Table(
    "build_author",
    db.Column(
        "build_id",
        GUID,
        db.ForeignKey("build.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "author_id",
        GUID,
        db.ForeignKey("author.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Build(RepositoryBoundMixin, StandardAttributes, db.Model):
    """
    A single build.

    Each Build contains many Jobs.
    """

    ref = db.Column(db.String, nullable=True)
    revision_sha = db.Column(db.String(40), nullable=True)

    number = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String, nullable=True)
    status = db.Column(Enum(Status), nullable=False, default=Status.unknown)
    result = db.Column(Enum(Result), nullable=False, default=Result.unknown)
    date_created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        default=timezone.now,
        server_default=func.now(),
        index=True,
    )
    date_started = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    date_finished = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    data = db.Column(JSONEncodedDict, nullable=True)
    provider = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String(64), nullable=True)
    hook_id = db.Column(
        GUID, db.ForeignKey("hook.id", ondelete="CASCADE"), nullable=True, index=True
    )
    url = db.Column(db.String, nullable=True)
    author_id = db.Column(
        GUID,
        db.ForeignKey("author.id", ondelete="SET NULL"),
        index=False,
        nullable=True,
    )

    authors = db.relationship(
        "Author", secondary=build_author_table, backref="builds", lazy="subquery"
    )
    revision = db.relationship(
        "Revision",
        foreign_keys="[Build.repository_id, Build.revision_sha]",
        viewonly=True,
    )
    hook = db.relationship("Hook")
    stats = db.relationship(
        "ItemStat",
        foreign_keys="[ItemStat.item_id]",
        primaryjoin="ItemStat.item_id == Build.id",
        viewonly=True,
        uselist=True,
    )
    failures = db.relationship(
        "FailureReason",
        foreign_keys="[FailureReason.build_id]",
        primaryjoin="FailureReason.build_id == Build.id",
        viewonly=True,
        uselist=True,
    )

    __tablename__ = "build"
    __table_args__ = (
        db.UniqueConstraint("repository_id", "number", name="unq_build_number"),
        db.UniqueConstraint(
            "repository_id", "provider", "external_id", name="unq_build_provider"
        ),
        db.ForeignKeyConstraint(
            ("repository_id", "revision_sha"),
            ("revision.repository_id", "revision.sha"),
        ),
        db.Index("idx_build_repo_sha", "repository_id", "revision_sha"),
        db.Index("idx_build_author_date", "author_id", "date_created"),
        db.Index(
            "idx_build_outcomes", "repository_id", "status", "result", "date_created"
        ),
    )
    __repr__ = model_repr("number", "status", "result")


@event.listens_for(Build.repository_id, "set", retval=False)
def set_number(target, value, oldvalue, initiator):
    if value is not None and target.number is None:
        target.number = select([func.next_item_value(value)])
    return value
