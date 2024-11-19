import ray
import requests
from fastapi import FastAPI
from ray import serve

app = FastAPI()


@serve.deployment
@serve.ingress(app)
class MyFastAPIDeployment:
    @app.get("/")
    def root(self):
        return "Hello, world!"

    @app.post("/{subpath}")
    def root(self, subpath: str):
        return f"Hello from {subpath}!"


serve.run(MyFastAPIDeployment.bind(), route_prefix="/hello")
resp = requests.post("http://localhost:8000/hello/Serve")
#assert resp.json() == "Hello from Serve!"
print(resp.json())