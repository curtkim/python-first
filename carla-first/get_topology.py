import carla
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

from common import load_world_if_needed


def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    load_world_if_needed(client, "/Game/Carla/Maps/Town01")
    world = client.get_world()
    map = world.get_map()
    pairs = map.get_topology()

    for pair in pairs:
        print(pair[0].road_id, pair[0].lane_id, pair[0].s, pair[0].transform.location, pair[0].is_junction,
              pair[1].road_id, pair[1].lane_id, pair[1].s, pair[1].transform.location, pair[1].is_junction)
    print(len(pairs))

    '''
    G = nx.Graph()
    G.add_edges_from([(pair[0].road_id, pair[1].road_id) for pair in pairs])
    print(G.nodes)
    path = nx.shortest_path(G, 10, 2)
    print('shortest_path', path)
    nx.draw(G, node_color="b", node_size=1, with_labels=True)
    plt.show()
    '''

    G2 = nx.Graph()
    G2.add_nodes_from([f"{pair[0].road_id}_{pair[0].lane_id}_{pair[1].road_id}_{pair[1].lane_id}" for pair in pairs])

    #pos = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1), 4: (0.5, 2.0)}
    pos = {f"{pair[0].road_id}_{pair[0].lane_id}_{pair[1].road_id}_{pair[1].lane_id}": (pair[0].transform.location.x, pair[0].transform.location.y*-1) for pair in pairs}
    nx.draw(G2, pos, node_color="b", node_size=1, with_labels=False)

    plt.show()

if __name__ == '__main__':
    main()
