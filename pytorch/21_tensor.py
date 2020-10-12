import torch


def test_scatter_add_():
    a = torch.arange(4, dtype=torch.float32).reshape(1, 4)
    b = torch.ones(2, 4).scatter_add_(0, torch.tensor([
        [0, 1, 1, 0]
    ]), a)

    assert b.equal(torch.Tensor([
        [1, 1, 1, 4],
        [1, 2, 3, 1],
    ]).type(torch.float32))


def test_index_select():
    a = torch.arange(12).reshape(3, 4)
    indices = torch.tensor([0, 2])
    assert torch.Tensor([
        [0, 1, 2, 3],
        [8, 9, 10, 11]
    ]).type(torch.int64).equal(torch.index_select(a, 0, indices))


