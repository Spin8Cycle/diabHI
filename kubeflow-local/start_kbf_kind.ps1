# Create a directory for configurations if it doesn't exist
New-Item -ItemType Directory -Path .\my-configs -Force

# Define the Kind cluster configuration
$kindConfigPath = '.\my-configs\kind-config.yaml'

$kindConfig = @"
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
"@

# Save the Kind configuration to a file
$kindConfig | Out-File -FilePath $kindConfigPath -Encoding utf8

# Create the Kind cluster using the configuration file
kind create cluster --name kfmanifest1 --config $kindConfigPath

# Get the kubeconfig for the cluster and save it
$kubeconfigPath = '.\my-configs\kfmanifest1-kubeflow-config'
kind get kubeconfig --name kfmanifest1 | Out-File -FilePath $kubeconfigPath -Encoding utf8

# Set the KUBECONFIG environment variable
$Env:KUBECONFIG = $kubeconfigPath

# Clone Kubeflow Manifests (Uncomment if needed)
# git clone https://github.com/kubeflow/manifests.git .

# Update the location of config.json file
docker login

# Path to Docker config.json
$dockerConfigPath = 'C:\Users\JCA\.docker\config.json'

# Create Kubernetes Secret for Docker Registry Credentials
kubectl create secret generic regcred `
    --from-file=.dockerconfigjson=$dockerConfigPath `
    --type=kubernetes.io/dockerconfigjson

# Deploy Kubeflow using Kustomize and Kubectl with a Retry Loop
do {
    kustomize build manifests/example | kubectl apply -f -
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Retrying to apply resources"
        Start-Sleep -Seconds 10
    }
} while ($LASTEXITCODE -ne 0)
