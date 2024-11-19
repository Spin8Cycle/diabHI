import time
from typing import Generator

import requests
from starlette.responses import StreamingResponse
from starlette.requests import Request

from ray import serve


@serve.deployment
class StreamingResponder:
    def generate_numbers(self, mx: int) -> Generator[str, None, None]:
        for i in range(mx):
            yield str(i)
            time.sleep(0.1)

    def __call__(self, request: Request) -> StreamingResponse:
        mx = request.query_params.get("max", "25")
        gen = self.generate_numbers(int(mx))
        return StreamingResponse(gen, status_code=200, media_type="text/plain")


serve.run(StreamingResponder.bind())

r = requests.get("http://localhost:8000?max=13", stream=True)
start = time.time()
r.raise_for_status()
for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
    print(f"Got result {round(time.time()-start, 1)}s after start: '{chunk}'")