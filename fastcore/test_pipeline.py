from fastcore.transform import Pipeline, Transform


@Transform
def f(x): return x + 1


@Transform
def g(x): return x / 2


def test_pipeline():
    pipe = Pipeline([f, g])
    assert 2.0 == pipe(3)
