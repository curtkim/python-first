import asyncio
import websockets
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


async def read_and_send(wsconn):
    session = PromptSession()
    while True:
        with patch_stdout():
            result = await session.prompt_async('> ')
        # print('> %s' % result)
        await wsconn.send(result)


async def recv_and_print(wsconn):
    while True:
        body = await wsconn.recv()
        print(f"< {body}")


async def main(loop):
    async with websockets.connect('ws://localhost:8080/echo') as wsconn:
        task1 = loop.create_task(read_and_send(wsconn))
        task2 = loop.create_task(recv_and_print(wsconn))
        await asyncio.wait([task1, task2])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

