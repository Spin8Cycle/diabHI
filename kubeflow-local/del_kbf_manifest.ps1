do {
    kustomize build manifests/example | kubectl delete -f -
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Retrying to apply resources"
        Start-Sleep -Seconds 10
    }
} while ($LASTEXITCODE -ne 0)