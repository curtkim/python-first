import torch
import torch.nn.functional as F


def test_l1_loss_1():
    assert torch.isclose(
        torch.FloatTensor([0.5]),
        F.l1_loss(torch.FloatTensor([1]), torch.FloatTensor([1.5]))
    )
    assert torch.isclose(
        torch.FloatTensor([0.5]),
        F.l1_loss(torch.FloatTensor([1, 2]), torch.FloatTensor([1.5, 2.5]))
    )

    # 2차원
    assert torch.isclose(
        torch.FloatTensor([0.5]),
        F.l1_loss(torch.FloatTensor([[1, 2], [3, 4]]), torch.FloatTensor([[1.5, 2.5], [3.5, 4.5]]))
    )


def test_smooth_l1_loss_1():
    assert torch.isclose(
        # torch.Tensor([0.125]),
        torch.FloatTensor([0.125]),  # https://pytorch.org/docs/stable/generated/torch.nn.SmoothL1Loss.html
        F.smooth_l1_loss(torch.FloatTensor([1]), torch.FloatTensor([1.5]))
    )
