import carla
import random
import time



def load_world_if_needed(client, map_name):
    if not map_name.endswith(client.get_world().get_map().name):
        client.load_world(map_name)
    else:
        print('current map is already ', map_name)

def remove_all_actors(world):
    actors = world.get_actors()
    for actor in actors:
        one_depth_type = actor.type_id.split(".")[0]
        if one_depth_type in ['vehicle', 'walker']:
            print('remove', actor.type_id, actor.id)
            actor.destroy()

def main():
    actor_list = []

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        load_world_if_needed(client, "/Game/Carla/Maps/Town02_Opt")

        world = client.get_world()
        remove_all_actors(world)

        world.unload_map_layer(carla.MapLayer.All)

        time.sleep(4)

    finally:

        print('destroying actors')
        actor_list.reverse()
        for actor in actor_list:
            print('destroy %s' % actor.type_id)
            if(isinstance(actor, carla.Sensor)):
                print('stop %s' % actor.type_id)
                actor.stop()
            actor.destroy()
        print('done.')


if __name__ == '__main__':

    main()
