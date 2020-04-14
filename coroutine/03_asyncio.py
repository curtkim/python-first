import asyncio
import datetime
import random
import threading

@asyncio.coroutine
def display_date(num, loop):
    end_time = loop.time() + 5.0
    while True:
        print("Loop: {} Time: {} thread={}".format(num, datetime.datetime.now(), threading.get_ident()))
        if (loop.time() + 1.0) >= end_time:
            break
        yield from asyncio.sleep(random.randint(0, 5))


loop = asyncio.get_event_loop()

asyncio.ensure_future(display_date(1, loop))
asyncio.ensure_future(display_date(2, loop))

loop.run_forever()
