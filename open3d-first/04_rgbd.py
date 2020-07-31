import open3d as o3d

if __name__ == "__main__":
    color_raw = o3d.io.read_image("test_data/RGBD/color/00000.jpg")
    depth_raw = o3d.io.read_image("test_data/RGBD/depth/00000.png")

    print(color_raw)
    print(depth_raw)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)
    print(rgbd_image)
    # color grayscale 0~1
    # depth float (16bit millimeter -> float meter)

    # o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
    # 640*480, focal_len (525, 525) center (319.5, 239.5)
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        o3d.camera.PinholeCameraIntrinsic(
            o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    # Flip it, otherwise the pointcloud will be upside down
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd])
