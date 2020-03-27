import asyncio
import aionotify

import functools
import rx
from rx.scheduler.eventloop import AsyncIOScheduler
from rx.disposable import Disposable


def from_aiter(iter, loop):
    def on_subscribe(observer, scheduler):
        async def _aio_sub():
            try:
                async for i in iter:
                    observer.on_next(i)
                loop.call_soon(
                    observer.on_completed)
            except Exception as e:
                loop.call_soon(
                    functools.partial(observer.on_error, e))

        task = asyncio.ensure_future(_aio_sub(), loop=loop)
        return Disposable(lambda: task.cancel())

    return rx.create(on_subscribe)


async def aiter(watcher):
    while(True):
        event = await watcher.get_event()
        yield event


async def main(loop):
    done = asyncio.Future()

    # Setup the watcher
    watcher = aionotify.Watcher()
    watcher.watch(alias='log', path='./tmp.log', flags=aionotify.Flags.MODIFY)
    await watcher.setup(loop)

    def on_completed():
        print("completed")
        done.set_result(0)

    disposable = from_aiter(aiter(watcher), loop).subscribe(
        on_next=lambda event: print("next: {}".format(event)),
        on_error=lambda e: print("error: {}".format(e)),
        on_completed=on_completed,
    )

    await done
    disposable.dispose()    



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))