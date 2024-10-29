# Define the Kustomize version you want to install
KUSTOMIZE_VERSION=$(curl -s "https://api.github.com/repos/kubernetes-sigs/kustomize/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")')

# Download the binary for your OS (Linux example shown)
curl -Lo kustomize "https://github.com/kubernetes-sigs/kustomize/releases/download/${KUSTOMIZE_VERSION}/kustomize_${KUSTOMIZE_VERSION}_linux_amd64.tar.gz"

# Extract the binary
tar -xzf kustomize_${KUSTOMIZE_VERSION}_linux_amd64.tar.gz
