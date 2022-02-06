import open3d as o3d
import numpy as np
import polyscope as ps

ps.init()

mesh = o3d.geometry.TriangleMesh.create_sphere()

vertices = np.asarray(mesh.vertices)
faces = np.asarray(mesh.triangles)

print(mesh)
print('Vertices:')
print(vertices)
print('Triangles:')
print(faces)

ps_mesh = ps.register_surface_mesh("my mesh", vertices, faces)
ps.show()

