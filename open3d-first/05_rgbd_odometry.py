import open3d as o3d
import numpy as np
import json

with open ("test_data/camera_primesense.json", "r") as myfile:
    print(json.load(myfile))

pinhole_camera_intrinsic = o3d.io.read_pinhole_camera_intrinsic("test_data/camera_primesense.json")
print(pinhole_camera_intrinsic.intrinsic_matrix)

source_color = o3d.io.read_image("test_data/RGBD/color/00000.jpg")
source_depth = o3d.io.read_image("test_data/RGBD/depth/00000.png")
target_color = o3d.io.read_image("test_data/RGBD/color/00001.jpg")
target_depth = o3d.io.read_image("test_data/RGBD/depth/00001.png")
source_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    source_color, source_depth)
target_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    target_color, target_depth)
target_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
    target_rgbd_image, pinhole_camera_intrinsic)


option = o3d.odometry.OdometryOption()
odo_init = np.identity(4)
print(option)

[success_color_term, trans_color_term, info] = o3d.odometry.compute_rgbd_odometry(
    source_rgbd_image, target_rgbd_image, pinhole_camera_intrinsic,
    odo_init, o3d.odometry.RGBDOdometryJacobianFromColorTerm(), option)

if success_color_term:
    print("Using RGB-D Odometry")
    print(trans_color_term)
    source_pcd_color_term = o3d.geometry.PointCloud.create_from_rgbd_image(
        source_rgbd_image, pinhole_camera_intrinsic)
    source_pcd_color_term.transform(trans_color_term)
    o3d.visualization.draw_geometries([target_pcd, source_pcd_color_term])


