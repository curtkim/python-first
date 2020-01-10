import numpy as np
import imageio

def make_point_cloud(depth, fx, fy, cx, cy):

    """Transform a depth image into a point cloud with one point for each
    pixel in the image, using the camera transform for a camera
    centred at cx, cy with field of view fx, fy.

    depth is a 2-D ndarray with shape (rows, cols) containing
    depths from 1 to 254 inclusive. The result is a 3-D array with
    shape (rows, cols, 3). Pixels with invalid depth in the input have
    NaN for the z-coordinate in the result.

    """
    rows, cols = depth.shape
    c, r = np.meshgrid(np.arange(cols), np.arange(rows), sparse=True)
    print('c.shape', c.shape)
    print('r.shape', r.shape)
    valid = (depth > 0) & (depth < 255)
    z = np.where(valid, depth / 256.0, np.nan)
    x = np.where(valid, z * (c - cx) / fx, 0)
    y = np.where(valid, z * (r - cy) / fy, 0)
    print(x.shape)
    print(y.shape)
    print(z.shape)
    return np.dstack((x, y, z))
    # shape must be n*3

image = imageio.imread("_out/depth_012740.png")
print(image.shape)
print(image.dtype)
print(image)

result = make_point_cloud(image, 0.01, 0.01, 400, 300)
print(result.shape)

out = open("temp.xyz", "w")

for row in result:
    if row[2] != np.nan:
        out.write("%.3f %.3f %.3f\n" % (row[0], row[1], row[2]))

out.close()