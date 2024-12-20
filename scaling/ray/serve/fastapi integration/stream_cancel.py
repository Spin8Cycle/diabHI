import asyncio
import time
from typing import AsyncGenerator

import requests
from starlette.responses import StreamingResponse
from starlette.requests import Request

from ray import serve


@serve.deployment
class StreamingResponder:
    async def generate_forever(self) -> AsyncGenerator[str, None]:
        try:
            i = 0
            while True:
                yield str(i)
                i += 1
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print("Cancelled! Exiting.")

    def __call__(self, request: Request) -> StreamingResponse:
        gen = self.generate_forever()
        return StreamingResponse(gen, status_code=200, media_type="text/plain")


serve.run(StreamingResponder.bind())

r = requests.get("http://localhost:8000?max=10", stream=True)
start = time.time()
r.raise_for_status()
for i, chunk in enumerate(r.iter_content(chunk_size=None, decode_unicode=True)):
    print(f"Got result {round(time.time()-start, 1)}s after start: '{chunk}'")
    if i == 11:
        print("Client disconnecting")
        break