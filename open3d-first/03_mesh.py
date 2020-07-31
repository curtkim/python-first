import copy
import numpy as np
import open3d as o3d

mesh = o3d.io.read_triangle_mesh('test_data/knot.ply')
print(mesh)
print(np.asarray(mesh.vertices))
print(np.asarray(mesh.triangles))

print(mesh.has_vertex_normals(),
      mesh.has_vertex_colors())
#o3d.visualization.draw_geometries([mesh])

mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])

mesh1 = copy.deepcopy(mesh)

mesh1.triangles = o3d.utility.Vector3iVector(
    np.asarray(mesh1.triangles)[:len(mesh1.triangles) // 2, :])
mesh1.triangle_normals = o3d.utility.Vector3dVector(
    np.asarray(mesh1.triangle_normals)[:len(mesh1.triangle_normals) //2, :])
#o3d.visualization.draw_geometries([mesh1])

mesh1.paint_uniform_color([1, 0.706, 0])
o3d.visualization.draw_geometries([mesh1])