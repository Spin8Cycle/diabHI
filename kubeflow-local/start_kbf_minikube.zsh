
# Start Minikube with Sufficient Resources
minikube start \
    --kubernetes-version=v1.30.0

# Clone Kubeflow Manifests
#git clone https://github.com/kubeflow/manifests.git .

# Update the location of config.json file
docker login
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=C:/Users/JCA/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson

# Deploy kubeflow using kustomize and kubectl
while ! kustomize build manifests/example | kubectl apply -f -; do
  echo "Retrying to apply resources"
  sleep 10
done