import numpy as np
import polyscope as ps
ps.init()

# generate some random nodes and edges between them
nodes = np.random.rand(100, 3)
edges = np.random.randint(0, 100, size=(250,2))

# visualize!
ps_net = ps.register_curve_network("my network", nodes, edges)
ps.show()

