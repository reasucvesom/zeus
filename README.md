# Zeus

**This project is under development.**

Zeus is a frontend and analytics provider for CI solutions. It is inspired by the work done at Dropbox on [Changes](https://github.com/dropbox/changes/).

The initial version aims to support Travis CI via GitHub, including:

- xunit
- code coverage
- artifacts (e.g. from ``py.test --html``)

## Setup

```shell
mkvirtualenv zeus --python `which python3`
make
createdb -E utf-8 zeus
zeus init
zeus db upgrade
zeus devserver
```

Now configure credentials by creating a GitHub account, and then add them to ``~/.zeus/zeus.conf.py``.

## Getting some data

```shell
$ zeus repos add https://github.com/getsentry/zeus.git
```

## Layout

```
zeus
├── setup.py  // server dependencies
├── zeus  // server code
├── templates  // server-rendered templates
├── public  // general static assets
├── package.json  // web client dependencies
└── webapp // web client
```

## Data Model

```
zeus
├── Repository
|   └── Build
|   ├   ├── Source
|   ├   └── Job
|   |       ├── Artifact
|   |       ├── FileCoverage
|   |       └── TestCase
|   └── Revision
|       ├── Author
|       └── Source
└── User
    └── Identity
```
