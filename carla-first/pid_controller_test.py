import carla
import random
import time

from shapely.geometry import Point, LineString

from carla_sync_mode import CarlaSyncMode
from pid_controller import VehiclePIDController
from common import find_waypoins


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
        client.set_timeout(5.0)

        load_world_if_needed(client, "/Game/Carla/Maps/Town01_Opt")

        world = client.get_world()
        remove_all_actors(world)
        world.unload_map_layer(carla.MapLayer.All)
        map = world.get_map()


        blueprint_library = world.get_blueprint_library()

        vehicle_bp = blueprint_library.find('vehicle.lincoln.mkz2017')
        vehicle_tf = carla.Transform(carla.Location(x=180, y=55, z=0.5), carla.Rotation(0, 180, 0))

        start_wp = map.get_waypoint(vehicle_tf.location)
        end_loc = carla.Location(x=158, y=27, z=0)
        waypoints = find_waypoins(start_wp, [10, 341, 25], 1, end_loc)
        route_line = LineString([(wp.transform.location.x, wp.transform.location.y) for wp in waypoints])
        print(route_line)

        vehicle = world.spawn_actor(vehicle_bp, vehicle_tf)

        _dt = 1.0 / 20.0
        _max_brake = 0.3
        _max_throt = 0.75
        _max_steer = 0.8
        args_lateral_dict = {
            'K_P': 0.8, #1.95,
            'K_D': 0, #1, #0.2,
            'K_I': 0.001, #0.07,
            'dt': _dt}
        args_longitudinal_dict = {
            'K_P': 1.0,
            'K_D': 0,
            'K_I': 0.05,
            'dt': _dt}
        _offset = 0

        vehicle_controller = VehiclePIDController(vehicle,
                                                        args_lateral=args_lateral_dict,
                                                        args_longitudinal=args_longitudinal_dict,
                                                        offset=_offset,
                                                        max_throttle=_max_throt,
                                                        max_brake=_max_brake,
                                                        max_steering=_max_steer)

        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(800))
        camera_bp.set_attribute('image_size_y', str(600))
        camera_bp.set_attribute('fov', str(90))
        camera_bp.set_attribute('sensor_tick', '0.033')
        camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=0, y=0, z=2.0), carla.Rotation(yaw=0)), attach_to=vehicle)


        frame = 0
        with CarlaSyncMode(world, camera, fps=20) as sync_mode:
            while True:
                curr_tf = vehicle.get_transform()
                curr_location = vehicle.get_location()
                #curr_velocity = vehicle.get_velocity()
                #curr_waypoint = map.get_waypoint(curr_location)

                DELTA = 2  # 2m 앞의 point를 보고 steer을 제어한다.
                distance = route_line.project(Point(curr_location.x, curr_location.y))
                next_point = route_line.interpolate(distance + DELTA)
                print('curr_loc', curr_location, 'next_point', next_point)
                next_waypoint = map.get_waypoint(carla.Location(next_point.x, next_point.y, 0))

                control = vehicle_controller.run_step(20, next_waypoint)
                vehicle.apply_control(control)

                snapshot, image = sync_mode.tick(timeout=2.0)
                #image.save_to_disk("_out/%05d_camera.png" % (frame))

                print(frame, vehicle.get_velocity(), control)
                spectator_tf = carla.Transform(carla.Location(curr_location.x, curr_location.y, curr_location.z + 2.5),
                                               curr_tf.rotation)
                world.get_spectator().set_transform(spectator_tf)
                frame += 1

                # 탈출조건
                if curr_location.distance(end_loc) < 3: break


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
