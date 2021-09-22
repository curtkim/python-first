import torch
import numpy as np

from liegroups.torch import SO2, utils


def test_from_matrix():
    C_good = SO2.from_matrix(torch.eye(2))
    print(C_good.mat)

    print(SO2.is_valid_matrix(C_good.mat))

    C_bad = SO2.from_matrix(torch.eye(2).add_(1e-3), normalize=True)
    print(isinstance(C_bad, SO2))
    print(C_bad.mat)


def test_from_angle():
    angle = torch.Tensor([np.pi / 2.])
    assert torch.allclose(torch.tensor([
        [0, -1],
        [1, 0]
    ], dtype=torch.float32), SO2.from_angle(angle).mat)


def test_from_angle_batch():
    angles = torch.Tensor([np.pi / 2., np.pi])

    assert torch.allclose(torch.tensor([
        [
            [0, -1],
            [1, 0]
        ],
        [
            [-1, 0],
            [0, 1]
        ],
    ], dtype=torch.float32), SO2.from_angle(angles).mat)


def test_dot():
    C = SO2(torch.Tensor([[0, -1],
                          [1, 0]]))
    pt = torch.Tensor([1, 2])

    assert torch.allclose(
        torch.tensor([-2, 1], dtype=torch.float32),
        C.dot(pt)
    )


def test_wedge():
    phi = torch.Tensor([1])
    assert torch.allclose(
        torch.tensor([
            [0, -1],
            [1, 0]
        ], dtype=torch.float32),
        SO2.wedge(phi)
    )


def test_left_jacobians():
    phi_small = torch.Tensor([0.])
    phi_big = torch.Tensor([np.pi / 2])

    assert torch.allclose(
        torch.tensor([
            [1, 0],
            [0, 1]
        ], dtype=torch.float32),
        SO2.left_jacobian(phi_small)
    )

    print(SO2.left_jacobian(phi_big))


def test_exp_log():
    C_big = SO2.exp(torch.Tensor([np.pi / 4]))

    torch.testing.assert_close(torch.tensor([
        [0.7071, -0.7071],
        [0.7071, 0.7071],
    ]), C_big.mat, rtol=1e-5, atol=1e-3)

    C_small = SO2.exp(torch.Tensor([0]))
    torch.testing.assert_close(torch.tensor([
        [1, -0],
        [0, 1],
    ], dtype=torch.float32), C_small.mat, rtol=1e-5, atol=1e-3)


def test_normalize():
    C = SO2.exp(torch.Tensor([np.pi / 4]))

    C.mat.add_(0.1)
    C.normalize()
    assert SO2.is_valid_matrix(C.mat).all()


def test_adjoint():
    C = SO2.exp(torch.Tensor([np.pi / 4]))
    assert (C.adjoint() == torch.Tensor([1.])).all()