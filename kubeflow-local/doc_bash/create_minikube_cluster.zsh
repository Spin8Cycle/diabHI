#!/bin/bash
# Start Minikube with config similar to kind-config
minikube start \
    --kubernetes-version=v1.31.0 \
    --cpus=2 \
    --memory=4096 \
    --extra-config=apiserver.service-account-issuer="kubernetes.default.svc" \
    --extra-config=apiserver.service-account-signing-key-file="/var/lib/minikube/certs/sa.key" \
    --extra-config=kubelet.cgroup-driver=systemd \
    --extra-config=apiserver.authorization-mode=RBAC

