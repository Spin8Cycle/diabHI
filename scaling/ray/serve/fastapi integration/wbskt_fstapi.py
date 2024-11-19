from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ray import serve

app = FastAPI()

@serve.deployment
@serve.ingress(app)
class EchoServer:
    @app.websocket("/")
    async def echo(self, ws: WebSocket):
        await ws.accept()
        try:
            while True:
                text = await ws.receive_text()
                await ws.send_text(text)
        except WebSocketDisconnect:
            print("Client disconnected.")


#serve_app = serve.run(EchoServer.bind())
echo = EchoServer.bind()