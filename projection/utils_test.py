import numpy as np
from utils import perspective, Plane, load_camera_params, bilinear_sampler

def test_perspective():
    extrinsic, intrinsic = load_camera_params('camera.json')
    P = intrinsic @ extrinsic
    plane = Plane(
        0, -1, 0,  # x, y, z
        0, 0, 0,  # roll, pitch, yaw
        3, 3, 2)  # col, row, scale

    print(perspective(plane.xyz, P, 3,3))

'''
def test_plane():
    plane = Plane(
        0, -1, 0,  # x, y, z
        0, 0, 0,  # roll, pitch, yaw
        3, 3, 2)  # col, row, scale

    print(plane.xyz.shape)
    print(plane.xyz)
'''