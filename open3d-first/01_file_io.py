import open3d as o3d

if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud("test_data/fragment.ply")
    print(pcd)
    o3d.io.write_point_cloud("tmp/copy_of_fragment.pcd", pcd)

    mesh = o3d.io.read_triangle_mesh("test_data/knot.ply")
    print(mesh)
    o3d.io.write_triangle_mesh("tmp/copy_of_knot.gltf", mesh)

    img = o3d.io.read_image('test_data/lena_color.jpg')
    print(img)
    o3d.io.write_image("tmp/copy_of_lena.jpg", img)