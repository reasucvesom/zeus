# k8s

This is just general rough documentation for things we've done. Assume its incomprehensible to most people.

Also, we are not kubernetes experts, so assume everything here is bad/wrong.

## Bootstrap

Apply zeus/\*.yaml

Create a cluster:

```bash
gcloud container clusters create zeus --num-nodes=3 --scopes https://www.googleapis.com/auth/devstorage.read_write
```

## Changing Scopes or Machine Specs

You'll need to create a new pool, and drain the old one:

https://cloud.google.com/kubernetes-engine/docs/tutorials/migrating-node-pool

```bash
gcloud container node-pools create pool-n1-standard-8 --cluster zeus --zone us-central1-b --scopes https://www.googleapis.com/auth/devstorage.read_write --machine-type=n1-standard-8 --num-nodes=1 --enable-autoupgrade --enable-autoscaling --max-nodes=40 --min-nodes=1
```

## Secrets

https://kubernetes.io/docs/concepts/configuration/secret/

For example, configuring SMTP password:

```
kubectl create secret generic mail --from-literal="password=VALUE"
```

## TODO

- Document secrets we define
- Turn all of Zeus into a helm chart?
