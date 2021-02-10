# This Python file uses the following encoding: utf-8

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import time

from carla_sync_mode import CarlaSyncMode


def load_world_if_needed(client, map_name):
    if not map_name.endswith(client.get_world().get_map().name):
        client.load_world(map_name)
    else:
        print('current map is already ', map_name)


def my_control(curr_tf, curr_velocity):
    return carla.VehicleControl(1, 0, 0.0, manual_gear_shift=True, gear=1)  # 1단으로 달린다.


def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)

        load_world_if_needed(client, "/Game/Carla/Maps/Town02")

        world = client.get_world()
        #world.set_weather(carla.WeatherParameters(cloudiness=20, sun_altitude_angle=45))
        # world.apply_settings(carla.WorldSettings(True, False, 1.0/30))
        map = world.get_map()

        start_tf = carla.Transform(carla.Location(x=40, y=110, z=0.5), carla.Rotation(0, 0, 0))
        start_wp = map.get_waypoint(start_tf.location)
        end_loc = carla.Location(x=140, y=110, z=0)

        blueprint_library = world.get_blueprint_library()
        bp = blueprint_library.find('vehicle.lincoln.mkz2017')

        vehicle = world.spawn_actor(bp, start_tf)
        print('created %s' % vehicle.type_id)

        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(800))
        camera_bp.set_attribute('image_size_y', str(600))
        camera_bp.set_attribute('fov', str(90))
        camera_bp.set_attribute('sensor_tick', '0.033')
        camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=0, y=0, z=2.0), carla.Rotation(yaw=0)), attach_to=vehicle)

        collision_bp = blueprint_library.find('sensor.other.collision')
        collision_detector = world.spawn_actor(collision_bp, carla.Transform(carla.Location(x=0, y=0, z=0), carla.Rotation(yaw=0)), attach_to=vehicle)
        def collision_callback(event):
            print("collision ", event.frame, event.timestamp, event.other_actor.id, event.other_actor.type_id)
        collision_detector.listen(collision_callback)


        print('===============')
        print('physics_control')
        print(vehicle.get_physics_control())

        vehicle.set_target_velocity(carla.Vector3D(-10, 0, 0)) # 초기 속도를 지정할 수 있다.

        start_time = time.process_time()
        frame = 0
        with CarlaSyncMode(world, camera, fps=10) as sync_mode:
            while True:
                curr_tf = vehicle.get_transform()
                curr_location = vehicle.get_location()
                curr_velocity = vehicle.get_velocity()
                waypoint = map.get_waypoint(curr_location)
                vehicle.apply_control(my_control(curr_tf, curr_velocity))

                snapshot, image = sync_mode.tick(timeout=2.0)
                image.save_to_disk("_out/%05d_camera.png" % (frame))

                spectator_tf = carla.Transform(carla.Location(curr_location.x, curr_location.y, curr_location.z + 2.5),
                                               curr_tf.rotation)
                world.get_spectator().set_transform(spectator_tf)
                frame += 1

                # 탈출조건
                if curr_location.distance(end_loc) < 3: break

        print(f"success elapsed_time={time.process_time() - start_time}")

    finally:
        camera.stop()
        camera.destroy()

        collision_detector.stop()
        collision_detector.destroy()

        print('destroying vehicle')
        vehicle.destroy()

        # synchronous_mode를 해제한다.
        world.apply_settings(carla.WorldSettings(False))
        print('done.')


if __name__ == '__main__':
    main()
