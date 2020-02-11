import asyncio
import numpy as np

async def unix_interval_client():
    reader, writer = await asyncio.open_unix_connection('/tmp/python_asyncio')

    while(True):
        data = await reader.read(100)
        a = np.frombuffer(data, dtype=np.uint8)
        print(a)

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(unix_interval_client())