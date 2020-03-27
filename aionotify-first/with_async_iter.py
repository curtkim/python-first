import asyncio
import aionotify


async def aiter(watcher):    
    while(True):
        event = await watcher.get_event()
        yield event


async def run(loop, watcher):
    async for event in aiter(loop, watcher):
        print(event)


async def main(loop):
    # Setup the watcher
    watcher = aionotify.Watcher()
    watcher.watch(alias='log', path='./tmp.log', flags=aionotify.Flags.MODIFY)
    await watcher.setup(loop)

    async for event in aiter(watcher):
        print(event)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))