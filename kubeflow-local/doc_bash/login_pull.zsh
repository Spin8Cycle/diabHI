docker login

kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=C:/Users/JCA/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson
