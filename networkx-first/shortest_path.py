import networkx as nx 
import numpy as np 
import itertools 

"""
shortest_path_length(weight=True) doesn't mean weight sum.
"""

np.random.seed(0) 
G = nx.complete_graph(3)

# UPDATE edge attr with 'weight'
edge_weight_dict = {(0, 1): 1.5, (0, 2): 3.5, (1, 2): 5.5}
nx.set_edge_attributes(G, edge_weight_dict, name='weight')

for u, v in itertools.combinations(G, 2): 
    # weight에 True를 넘겨줬습니다.
    s_p = nx.shortest_path(G, u, v, weight=True)
    print(f"== shortest path        from node {u} to node {v} :: {s_p}")
    s_p_l = nx.shortest_path_length(G, u, v, weight=True)
    print(f"== shortest path length from node {u} to node {v} :: {s_p_l}")