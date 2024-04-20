# 1 million requests in Python

## Aims
- Saw a [blog post](https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html) by Pawel Miech a long time ago, always wanted to try it
- Also was wondering how it would be like if I did it in Scala using Cats Effect and fs2
- This experiment is a prequel to trying the 1 million requests challenge in Scala

## Experiment Parameters
- Run an async server where each request is handled with a random duration between 0s and *n*s
- Send *r* requests to the server with *s* semaphores and record the duration *d*s
- Record duration of 1 million and 10 million requests
- *n* = 1s, 2s, 3s  
- *r* = 1000, 3000, 10000, 30000, 100000, 300000
- *s* = 1000, 2000, 4000, 6000, 8000, 10000

