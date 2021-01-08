import threading
from contextvars import ContextVar
from async_btree import FAILURE, SUCCESS, decision, fallback, repeat_until, selector, sequence


async def a_func():
    print("\ta_func " + str(threading.get_ident()))
    return 'a'


async def b_func():
    print("\tb_func " + str(threading.get_ident()))
    return 'b'


async def failure_func():
    print("\tfailure_func " + str(threading.get_ident()))
    return FAILURE


async def success_func():
    print("\tsuccess_func " + str(threading.get_ident()))
    return SUCCESS


async def exception_func():
    print("\texception_func " + str(threading.get_ident()))
    raise RuntimeError("ops")


def test_repeat_until_falsy_condition(kernel):

    counter = ContextVar('counter', default=5)

    async def tick():
        value = counter.get()
        counter.set(value - 1)
        if value <= 0:
            return FAILURE
        if value == 3:
            raise RuntimeError('3')
        return SUCCESS

    assert kernel.run(repeat_until(condition=tick, child=a_func)) == 'a', 'return last sucess result'
    assert counter.get() == 2


from curio import Kernel
k = Kernel()

tree1 = sequence(children=[a_func, failure_func, success_func])
r = k.run(tree1)
print(f"result={r}")

tree2 = selector(children=[exception_func, failure_func, a_func])
r = k.run(tree2)
print(f"result={r}")

assert k.run(decision(condition=success_func, success_tree=a_func)) == 'a'
print("===")
test_repeat_until_falsy_condition(k)

k.run(shutdown=True)

