import asyncio
from aiohttp import ClientSession, TCPConnector
import time
from itertools import product
from argparse import ArgumentParser

async def fetch(url, session):
    async with session.get(url) as response:
        
        return await response.text()


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(r, s):
    url = "http://localhost:8000/{}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(s)
    
    connector = TCPConnector(limit = 0)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession(connector = connector) as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses
        
parser = ArgumentParser()
parser.add_argument("maxD", default=2, type=float)
parser.add_argument("--t", help="Flag to indicate whether this is the testing phase", action="store_true")

if __name__  == "__main__":
    
    args = parser.parse_args()
    MAX_DELAY = args.maxD
    if args.t:
        output_path = f"results/results_maxDelay={MAX_DELAY}s.csv"
    else:
        output_path = "results/results.csv"
    
    print(f"Max delay = {MAX_DELAY}")
    
    if args.t:
        # During testing phase, we run over a range of smaller number of requests and semaphore counts
        rs = [1000, 3000, 10000, 30000, 100000, 300000]
        sems = [1000, 2000, 4000, 6000, 8000, 10000]
    else:
        # During the final results phase, we run for a large number of requests but fix the semaphore count
        rs = [1000000, 10000000]
        sems = [5000]
    
    with open(output_path, "w") as f:
        f.write("r, s, d\n")
    
    for r, s in product(rs, sems):
        
        start = time.monotonic()
        asyncio.run(run(r, s))
        duration = time.monotonic() - start
        
        with open(output_path, "a") as f:
            f.write(f"{r}, {s}, {duration}\n")
    
        print(f"{r} requests | {s} semaphore | {duration}s")