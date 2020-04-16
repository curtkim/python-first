import threading
from curio import sleep
from curio import Kernel
from async_btree import FAILURE, parallele


async def a_func():
    print("\ta_func " + str(threading.get_ident()))
    await sleep(0.5)
    return 'a'


async def b_func():
    print("\tb_func " + str(threading.get_ident()))
    await sleep(1)
    return 'b'


async def failure_func():
    print("\tfailure_func " + str(threading.get_ident()))
    await sleep(0.75)
    return FAILURE


k = Kernel()

tree = parallele(children=[a_func, b_func])
result = k.run(tree)
print(f"result={result}")

k.run(shutdown=True)

