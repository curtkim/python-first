import copy
import numpy as np
import torch
from torch import tensor

from liegroups.torch import SE2, SO2, utils


def test_from_matrix():
    T_good = SE2.from_matrix(torch.eye(3))

    print(T_good.rot.mat)
    torch.allclose(tensor([
        [1, 0],
        [0, 1],
    ], dtype=torch.float32), T_good.rot.mat)
    torch.allclose(tensor([0, 0], dtype=torch.float32), T_good.trans)

    assert isinstance(T_good, SE2) \
        and isinstance(T_good.rot, SO2) \
        and T_good.trans.shape == (2,)


def test_dot():
    T = torch.Tensor([[0, -1, -0.5],
                      [1, 0, 0.5],
                      [0, 0, 1]])
    T_SE2 = SE2.from_matrix(T)
    torch.allclose(tensor([np.pi / 2], dtype=torch.float32), T_SE2.rot.to_angle())
    torch.allclose(tensor([-0.5, 0.5], dtype=torch.float32), T_SE2.trans)

    pt = torch.Tensor([1, 2])
    Tpt_SE2 = T_SE2.dot(pt)
    torch.allclose(tensor([-2 -0.5, 1 + 0.5], dtype=torch.float32), Tpt_SE2)

    pth = torch.Tensor([1, 2, 1])
    Tpth_SE2 = T_SE2.dot(pth)
    torch.allclose(tensor([-2 - 0.5, 1 + 0.5, 1], dtype=torch.float32), Tpth_SE2)


def test_exp_log():
    T = SE2.exp(torch.Tensor([1, 2, 3]))
    print(T.trans)
    print(T.rot.to_angle())
    assert utils.allclose(SE2.exp(SE2.log(T)).as_matrix(), T.as_matrix())
