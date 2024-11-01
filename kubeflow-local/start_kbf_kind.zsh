
# Start Kind
cat <<EOF | kind create cluster --name=kfmanifest1 --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  image: kindest/node:v1.31.0@sha256:53df588e04085fd41ae12de0c3fe4c72f7013bba32a20e7325357a1ac94ba865
  kubeadmConfigPatches:
  - |
    kind: ClusterConfiguration
    apiServer:
      extraArgs:
        "service-account-issuer": "kubernetes.default.svc"
        "service-account-signing-key-file": "/etc/kubernetes/pki/sa.key"
EOF

kind get kubeconfig --name kfmanifest1 > ./my-configs/kfmanifest1-kubeflow-config
export KUBECONFIG=./my-configs/kfmanifest1-kubeflow-config

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