KFP_ENV=platform-agnostic
kustomize build cluster-scoped-resources/ | kubectl apply -f -
kubectl wait crd/applications.app.k8s.io --for condition=established --timeout=60s
kustomize build "env/${KFP_ENV}/" | kubectl apply -f -
kubectl wait pods -l application-crd-id=kubeflow-pipelines -n kubeflow --for condition=Ready --timeout=1800s
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80