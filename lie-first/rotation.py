import math
import torch
import sys
import nnp.so3 as so3

rx = torch.tensor([1., 0., 0.], dtype=torch.float)
ry = torch.tensor([0., 1., 0.], dtype=torch.float)
rz = torch.tensor([0., 0., 1.], dtype=torch.float)
points = torch.vstack([rx, ry, rz])

axis = torch.ones(3) / math.sqrt(3) * (math.pi * 2 / 3)
print(axis)
R = so3.rotate_along(axis)

rotated = (R @ points.t()).t()

def test_rotated_unit_vectors():
    expected = torch.vstack([ry, rz, rx])
    assert torch.allclose(rotated, expected, atol=1e-5)

