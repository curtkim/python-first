import numpy as np
import polyscope as ps
ps.init()

vertices = np.random.rand(100, 3) # (V,3) vertex position array
faces = np.random.randint(0, 100, size=(250,3)) # (F,3) array of indices 
                                                # for triangular faces

# visualize!
ps_mesh = ps.register_surface_mesh("my mesh", vertices, faces)
ps.show()

