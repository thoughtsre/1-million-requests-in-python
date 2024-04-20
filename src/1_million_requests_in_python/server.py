import asyncio
from datetime import datetime
from aiohttp import web
import random
from argparse import ArgumentParser

random.seed(1)

parser = ArgumentParser()
parser.add_argument("maxD", default=1, type=float)

if __name__ == "__main__":
    
    maxD = parser.parse_args().maxD
    
    async def hello(request):
    
        delay = random.uniform(0, maxD)
        
        await asyncio.sleep(delay)
        
        request_id = request.match_info["id"]
        
        response = web.Response(body=f"Request {request_id}")
        
        return response
    
    print(f"Serving with max delay of {maxD}s")

    app = web.Application()
    app.add_routes([web.get("/{id}", hello)])
    web.run_app(app, port=8000)