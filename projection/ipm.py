import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils import perspective, Plane, load_camera_params, bilinear_sampler

image = cv2.cvtColor(cv2.imread('stuttgart_01_000000_003715_leftImg8bit.png'), cv2.COLOR_BGR2RGB)
TARGET_H, TARGET_W = 500, 500

def ipm_from_parameters(image, xyz, K, RT):
    P = K @ RT

    print('K.shape', K.shape)
    print('RT.shape', RT.shape)
    print('P.shape', P.shape)

    pixel_coords = perspective(xyz, P, TARGET_H, TARGET_W)
    print('pixel_coords.shape', pixel_coords.shape)
    print('pixel_coords[0,0]', pixel_coords[250,250])
    image2 = bilinear_sampler(image, pixel_coords)
    return image2.astype(np.uint8)


if __name__ == '__main__':

    # Define the plane on the region of interest (road)
    plane = Plane(
        0, -25, 0,                      #x, y, z
        0, 0, 0,                        #roll, pitch, yaw
        TARGET_H, TARGET_W, 0.1)        #col, row, scale
    assert plane.xyz.shape == (4, 250000)
    print(plane.xyz)

    extrinsic, intrinsic = load_camera_params('camera.json')
    warped1 = ipm_from_parameters(image, plane.xyz, intrinsic, extrinsic)

    plt.figure(figsize=(20, 20))
    plt.imshow(warped1)
    plt.show()

    '''
    ################
    # OpenCV
    ################
    # Vertices coordinates in the source image
    s = np.array([[830, 598],
                  [868, 568],
                  [1285, 598],
                  [1248, 567]], dtype=np.float32)

    # Vertices coordinates in the destination image
    t = np.array([[177, 231],
                  [213, 231],
                  [178, 264],
                  [216, 264]], dtype=np.float32)

    # Warp the image
    warped2 = ipm_from_opencv(image, s, t)
    plt.imshow(warped2)
    '''
