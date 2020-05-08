# https://rednafi.github.io/digressions/python/2020/04/05/python-singledispatch.html
# single_dispatch.py
from functools import singledispatch


@singledispatch
def process(num=None):
    raise NotImplementedError("Implement process function.")


@process.register(int)
def sub_process(num):
    # processing interger
    return f"Integer {num} has been processed successfully!"


@process.register(float)
def sub_process(num):
    # processing float
    return f"Float {num} has been processed successfully!"


# use the function
print(process(12.0))
print(process(1))