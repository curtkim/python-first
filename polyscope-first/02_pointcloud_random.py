import numpy as np
import polyscope as ps
ps.init()

# generate some points
points = np.random.rand(100, 3)

# visualize!
ps_cloud = ps.register_point_cloud("my points", points)
ps.show()

# with some options
ps_cloud_opt = ps.register_point_cloud("my points", points, 
                                       radius=0.02, point_render_mode='quad')
ps.show()

