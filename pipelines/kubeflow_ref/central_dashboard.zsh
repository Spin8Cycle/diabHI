export ISTIO_NAMESPACE=istio-system
kubectl port-forward svc/istio-ingressgateway -n ${ISTIO_NAMESPACE} 8000:80