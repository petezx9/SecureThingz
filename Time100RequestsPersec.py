#!/usr/bin/env python3
#
# Doh, i read the task wrong,
# I've made 100 requests per 1 sec, and reported mean an max times
# of every batch of 100
#
# Still you might like to see it :-)
#
import asyncio
import time
import numpy as np
from aiohttp import ClientSession

# An interval sleeper
async def interval(secs):
    time.sleep(secs)

# get a url and time the full return time.
# return time to respond
async def fetch(url, session):
    async with session.get(url) as response:
        start = time.time()
        await response.read()
        return time.time() - start

# make a number of url calls tasks and run them asynchronously
# a long side async interval task.
# gather async results
# return mean of results,
async def run(IntervalSecs, r, url):
    tasks = []
    async with ClientSession() as session:  # share session between tasks
        # make up a batch of 100 calls
        for i in range(r):
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)  # fire off all 100 calls.
        # and interval, a simple interval method as long as responses come back with interval, otherwise interval will become length of longest request.
        await interval(IntervalSecs)
        # we'll not move on until tasks and interval have finished

    # report mean and max
    print('mean:', np.mean(responses), ' Max:', np.max(responses))


url = "https://www.telegraph.co.uk/rugby-union/"
NumRequests = 100 #batch size
IntervalSecs = 1  # seconds
# get an event loop for async calls and run tasks in batches.
while True:
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(IntervalSecs, NumRequests, url))
    loop.run_until_complete(future)
