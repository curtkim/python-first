import asyncio
import aionotify

# Setup the watcher
watcher = aionotify.Watcher()
watcher.watch(alias='log', path='./tmp.log', flags=aionotify.Flags.MODIFY)

# Prepare the loop
loop = asyncio.get_event_loop()

async def work():
    await watcher.setup(loop)
    for _i in range(10):
        # Pick the 10 first events
        event = await watcher.get_event()
        print(event)
    watcher.close()

loop.run_until_complete(work())
loop.stop()
loop.close()
