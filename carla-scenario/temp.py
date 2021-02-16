import carla
import time

from carlax.common import find_waypoins, remove_all_actors, load_world_if_needed


def main():

    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    load_world_if_needed(client, "/Game/Carla/Maps/Town01_Opt")

    world = client.get_world()
    remove_all_actors(world)
    world.unload_map_layer(carla.MapLayer.All)
    map = world.get_map()

    next_waypoint = map.get_waypoint(carla.Location(x=180, y=55, z=0.5))
    print(next_waypoint)



if __name__ == '__main__':
    main()