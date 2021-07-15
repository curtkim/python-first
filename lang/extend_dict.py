def test_extend_dict():
    defaults = {
        "a": 0.001,
        "b": [1, 2]
    }
    kwargs = {
        "a": 0.1
    }

    assert {
        "a": 0.1,
        "b": [1, 2]
    } == {**defaults, **kwargs}
