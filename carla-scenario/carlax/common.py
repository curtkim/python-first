import carla


def remove_all_actors(world):
    actors = world.get_actors()
    for actor in actors:
        one_depth_type = actor.type_id.split(".")[0]
        if one_depth_type in ['vehicle', 'walker']:
            print('remove', actor.type_id, actor.id)
            actor.destroy()


def destroy_actors(*actors):
    print('destroying actors')
    for actor in actors:
        if (isinstance(actor, carla.Sensor)):
            print('stop %s' % actor.type_id)
            actor.stop()

        print('destroy %s' % actor.type_id)
        actor.destroy()
    print('destroying actors done.')


def load_world_if_needed(client, map_name):
    if not map_name.endswith(client.get_world().get_map().name):
        client.load_world(map_name)
    else:
        print('current map is already ', map_name)
