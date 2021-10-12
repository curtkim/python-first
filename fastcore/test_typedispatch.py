import numbers

from fastcore.dispatch import typedispatch


@typedispatch
def _f(x:numbers.Integral, y): return x+1

@typedispatch
def _f(x:int, y:float): return x+y


def test_typedispatch():
    assert 4 == _f(3,2)
    assert 5.0 == _f(3,2.0)