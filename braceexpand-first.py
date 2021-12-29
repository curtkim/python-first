from braceexpand import braceexpand


def test_braceexpand():
    assert [
        'pangyo_front_main-train-000005.tar',
        'pangyo_front_main-train-000006.tar',
        'pangyo_front_main-val-000000.tar',
        'pangyo_front_main-val-000001.tar',
    ] == list(braceexpand('{pangyo_front_main-train-{000005..00006}.tar,pangyo_front_main-val-{000000..00001}.tar}'))
