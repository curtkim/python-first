import numpy as np
import open3d as o3d
import json

if __name__ == "__main__":
    pcd = o3d.io.read_point_cloud("test_data/fragment.ply")
    print(np.asarray(pcd.points))
    #o3d.visualization.draw_geometries([pcd])

    downpcd = pcd.voxel_down_sample(0.05)
    #o3d.visualization.draw_geometries([downpcd])

    downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.1, max_nn=30))
    print(downpcd.has_colors())
    print(downpcd.has_normals())
    #o3d.visualization.draw_geometries([downpcd])

    print("Print a normal vector of the 0th point")
    print(downpcd.normals[0])
    print("Print the normal vectors of the first 10 points")
    print(np.asarray(downpcd.normals)[:10, :])
    print("")

    ###
    with open('test_data/cropped.json') as json_file:
        data = json.load(json_file)
        print(data)

    vol = o3d.visualization.read_selection_polygon_volume("test_data/cropped.json")
    chair = vol.crop_point_cloud(pcd)
    #o3d.visualization.draw_geometries([chair])

    chair.paint_uniform_color([1, 0.706, 0])
    print(chair.has_colors())
    o3d.visualization.draw_geometries([chair])
