import asyncio
import concurrent.futures
import threading

def blocking_io():
    print(threading.get_ident())
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)

def cpu_bound():
    print(threading.get_ident())
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 10))

async def main():
    print("main", threading.get_ident())
    loop = asyncio.get_running_loop()

    ## Options:

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        result = await loop.run_in_executor(
            pool, cpu_bound)
        print('custom process pool', result)

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(
        None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool', result)


asyncio.run(main())