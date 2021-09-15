import torch
from torch import tensor
from utils import find_intersection, find_jaccard_overlap

t1_box1 = tensor([
    [0.8, 0.1, 1.0, 0.3]
])
t1_box2 = tensor([
    [0.9, 0.2, 1.0, 0.4],
    [0, 0, 1, 1]
])


def test_find_intersection():
    assert torch.allclose(tensor([
        [0.01, 0.04]
    ]), find_intersection(t1_box1, t1_box2))


# iou를 계산한다.
def test_find_jaccard_overlap():
    assert torch.allclose(tensor([
        [0.2, 0.04]
    ]), find_jaccard_overlap(t1_box1, t1_box2))

    # overlap_for_each_prior, object_for_each_prior = find_jaccard_overlap(t1_box1, t1_box2).max(dim=0)
    # print(overlap_for_each_prior, object_for_each_prior)


def test_torch_tensor_max():
    a = tensor([
        [1, 2, 3],
        [4, 5, 6]
    ])

    values, indeces = a.max(dim=0)
    assert torch.equal(tensor([4, 5, 6]), values)
    assert torch.equal(tensor([1, 1, 1]), indeces)

    values1, indeces1 = a.max(dim=1)
    assert torch.equal(tensor([3, 6]), values1)
    assert torch.equal(tensor([2, 2]), indeces1)
