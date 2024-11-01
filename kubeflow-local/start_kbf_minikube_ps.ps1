minikube start --kubernetes-version=v1.30.0

# git clone https://github.com/kubeflow/manifests.git .

docker login
$dockerConfigPath = 'C:\Users\JCA\.docker\config.json'
kubectl create secret generic regcred `
    --from-file=.dockerconfigjson=$dockerConfigPath `
    --type=kubernetes.io/dockerconfigjson

do {
    kustomize build manifests/example | kubectl apply -f -
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Retrying to apply resources"
        Start-Sleep -Seconds 10
    }
} while ($LASTEXITCODE -ne 0)