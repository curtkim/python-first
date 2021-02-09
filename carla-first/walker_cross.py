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

        load_world_if_needed(client, "/Game/Carla/Maps/Town02")

        world = client.get_world()
        remove_all_actors(world)

        # 1. walker, vehicle
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.find('vehicle.lincoln.mkz2017')
        walker_bp = blueprint_library.find('walker.pedestrian.0001')
        #walker_controller_bp = blueprint_library.find('controller.ai.walker')

        start_tf = carla.Transform(carla.Location(x=100, y=103, z=2.5), carla.Rotation(0, 90, 0))
        vehicle_tf = carla.Transform(carla.Location(x=100, y=111, z=0.5), carla.Rotation(0, 0, 0))

        walker = world.spawn_actor(walker_bp, start_tf)
        print(walker.bounding_box)
        #walker_controller = world.spawn_actor(walker_controller_bp, start_tf, walker)
        vehicle = world.spawn_actor(vehicle_bp, vehicle_tf)

        actor_list.append(walker)
        actor_list.append(vehicle)
        #actor_list.append(walker_controller)
        print('created %s' % walker.type_id)
        #print('created %s' % walker_controller.type_id)

        # 1.5 static.prop.constructioncone
        cone_bp = blueprint_library.find('static.prop.constructioncone')
        cone = world.spawn_actor(cone_bp, carla.Transform(carla.Location(x=102, y=107, z=0.5), carla.Rotation(0, 0, 0)))
        actor_list.append(cone)

        # 2. sensor
        collision_bp = blueprint_library.find('sensor.other.collision')
        collision_detector = world.spawn_actor(collision_bp, carla.Transform(carla.Location(x=0, y=0, z=0), carla.Rotation(yaw=0)), attach_to=walker)
        actor_list.append(collision_detector)
        print('created %s' % collision_detector.type_id)

        def callback(event):
            print("collision ", event.frame, event.timestamp, event.other_actor.id, event.other_actor.type_id)
        collision_detector.listen(callback)

        # 3. apply_control
        walker.apply_control(carla.WalkerControl(carla.Vector3D(0.0, 1.0, 0.0), 1.4, False))
        #walker_controller.set_max_speed(0.1)
        #walker_controller.go_to_location(carla.Location(x=115, y=302.5, z=0.5))
        #walker_controller.start()

        # 4. etc
        spectator_tf = carla.Transform(carla.Location(x=100, y=107.5, z=10), carla.Rotation(-90, -90, 0))
        world.get_spectator().set_transform(spectator_tf)
        
        world.debug.draw_arrow(
            carla.Location(x=100, y=103, z=0.5),
            carla.Location(x=100, y=111, z=0.5),
            0.3,
            0.5,
            carla.Color(255,0,0,0),
            10,
        )
        time.sleep(3)
        print(walker.bounding_box)        
        world.debug.draw_box(
            carla.BoundingBox(walker.get_transform().location, walker.bounding_box.extent),
            walker.get_transform().rotation, 
            1, 
            carla.Color(255,0,0,127),
            1.0)
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
    print('last sleep')
