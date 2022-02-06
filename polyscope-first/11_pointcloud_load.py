import open3d as o3d
import numpy as np

import polyscope as ps
ps.init()

# generate some points
pcd = o3d.io.read_point_cloud("../open3d-first/test_data/fragment.ply")
points = np.asarray(pcd.points)

# visualize!
ps_cloud = ps.register_point_cloud("my points", points)
ps.show()

# with some options
ps_cloud_opt = ps.register_point_cloud("my points", points, 
                                       radius=0.02, point_render_mode='quad')
ps.show()
