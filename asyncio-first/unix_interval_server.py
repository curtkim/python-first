import asyncio

i = 0

async def handle_interval(reader, writer):
    global  i
    while(i < 100):
        writer.write(str(i).encode())
        await writer.drain()
        i += 1
        await asyncio.sleep(1)
    writer.close()

async def main():
    server = await asyncio.start_unix_server(
        handle_interval, '/tmp/python_asyncio')

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())