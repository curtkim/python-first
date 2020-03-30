import copy
import numpy as np
import open3d as o3d

import carla
import random
import time

def load_world_if_needed(client, map_name):
    if not map_name.endswith(client.get_world().get_map().name):
        client.load_world(map_name)
    else:
        print('current map is already ', map_name)


def main():
    actor_list = []

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        load_world_if_needed(client, "/Game/Carla/Maps/Town03")

        world = client.get_world()

        blueprint_library = world.get_blueprint_library()
        bp = random.choice(blueprint_library.filter('vehicle'))

        transform = carla.Transform(carla.Location(x=40, y=-3.2, z=1), carla.Rotation())
        vehicle = world.spawn_actor(bp, transform)
        vehicle.attributes['role_name'] == "ego"

        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)

        # gnss
        gnss_bp = world.get_blueprint_library().find('sensor.other.gnss')
        gnss_sensor = world.spawn_actor(gnss_bp, carla.Transform(carla.Location(x=0, y=0, z=0)), attach_to=vehicle)
        actor_list.append(gnss_sensor)
        print('created %s' % gnss_sensor.type_id)

        def gnss_callback(measurement):
            print(f"""gnss frame={measurement.frame} transform={measurement.transform} {measurement.latitude:.2f} {measurement.longitude:.2f} {measurement.altitude:.2f}""")

        gnss_sensor.listen(gnss_callback)

        # imu
        imu_bp = world.get_blueprint_library().find('sensor.other.imu')
        imu_sensor = world.spawn_actor(imu_bp, carla.Transform(carla.Location(x=0, y=0, z=0)), attach_to=vehicle)
        actor_list.append(imu_sensor)
        print('created %s' % imu_sensor.type_id)

        def imu_callback(measurement):
            print(f"""imu  frame={measurement.frame} transform={measurement.transform} accelerometer={measurement.accelerometer} gyroscope={measurement.gyroscope} compass={measurement.compass}""")

        imu_sensor.listen(imu_callback)

        # collision     
        collision_bp = world.get_blueprint_library().find('sensor.other.collision')
        collision_sensor = world.spawn_actor(collision_bp, carla.Transform(carla.Location(x=0, y=0, z=0)), attach_to=vehicle)
        actor_list.append(collision_sensor)
        print('created %s' % collision_sensor.type_id)

        def collision_callback(measurement):
            print(f"""coll frame={measurement.frame} transform={measurement.transform} actor={measurement.actor} other_actor={measurement.other_actor}""")

        collision_sensor.listen(collision_callback)


        time.sleep(3)

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
    time.sleep(2)
