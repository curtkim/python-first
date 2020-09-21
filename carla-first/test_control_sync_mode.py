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


import base64
import json

import carla
import time
import numpy as np
import math
from shapely.geometry import Point, LineString

from carla_sync_mode import CarlaSyncMode
from utils import tf2matrix4list

WIDTH = 2560
HEIGHT = 1440

UNIT_WIDTH = int(WIDTH / 3)
UNIT_HEIGHT = int(HEIGHT / 3)

CAMERA_CONFIGS = [
    # [tranform, fov]
    [carla.Transform(carla.Location(x=1.5, y=0, z=2.4), carla.Rotation(yaw=0)), 120],   # front120
    [carla.Transform(carla.Location(x=1.5, y=0.1, z=2.4), carla.Rotation(yaw=0)), 90],  # front90
    [carla.Transform(carla.Location(x=0, y=1.1, z=2.4), carla.Rotation(yaw=45)), 90],   # right1
    [carla.Transform(carla.Location(x=1.0, y=1.1, z=1), carla.Rotation(yaw=135)), 120], # right2
    [carla.Transform(carla.Location(x=-1.5, y=0, z=2.4), carla.Rotation(yaw=180)), 120],# back
    [carla.Transform(carla.Location(x=1.0, y=-1.1, z=1), carla.Rotation(yaw=225)), 120],# left1
    [carla.Transform(carla.Location(x=0, y=-1.1, z=2.4), carla.Rotation(yaw=315)), 90], # left2
    [carla.Transform(carla.Location(x=1.5, y=-0.1, z=2.4), carla.Rotation(yaw=0)), 45], # front45
]

def make_sensor(world, vehicle, rgb_bp, tf, fov):
    rgb_bp.set_attribute('image_size_x', str(UNIT_WIDTH))
    rgb_bp.set_attribute('image_size_y', str(UNIT_HEIGHT))
    rgb_bp.set_attribute('fov', str(fov))
    rgb_bp.set_attribute('sensor_tick', '0.033')
    return world.spawn_actor(rgb_bp, tf, attach_to=vehicle)


def load_world_if_needed(client, map_name):
    if not map_name.endswith(client.get_world().get_map().name):
        client.load_world(map_name)
    else:
        print('current map is already ', map_name)


def print_waypoint(wp):
    print(f"road={wp.road_id}, section=${wp.section_id}, lane={wp.lane_id}, s=${wp.s} ${wp}")


def find_waypoins(start, trace_road_ids, interval, end_loc):
    """
        start부터 end_loc까지 trace_road_ids를 따라서 interval간격으로 waypoints를 생성해서 반환한다.

        start: start waypoint
        trace_road_ids: road_id의 리스트(순서가 중요함, 중복가능)
        interval : 반환되는 waypoint의 interval(단위 meter)
        end_loc : end location의 3m안에 들아가면 종료된다.
    """
    results = [start]
    curr = start
    road_idx = 0
    road_ids = trace_road_ids[road_idx:road_idx+2]

    while( curr.transform.location.distance(end_loc) > 3):
        candidates = curr.next(interval)
        filtered = [c for c in candidates if c.road_id in road_ids]
        if len(filtered) != 1:
            print('failed count=', len(filtered))
            print('candidates road_ids', [c.road_id for c in candidates])
            break        
        curr = filtered[0]
        print(road_ids, curr.road_id, curr.s)
        #print_waypoint(curr)
        results.append(curr)
        if road_ids.index(curr.road_id) == 1:
            road_idx += 1
            road_ids = trace_road_ids[road_idx:road_idx+2]

    return results


def my_control(curr_tf, curr_velocity, route_line):
    DELTA = 2 # 2m 앞의 point를 보고 steer을 제어한다.

    curr_location = curr_tf.location
    distance = route_line.project(Point(curr_location.x, curr_location.y))
    next_point = route_line.interpolate(distance + DELTA)
        
    curr_angle = -1*curr_tf.rotation.yaw
    new_angle = math.atan2(-1*(next_point.y - curr_location.y), next_point.x - curr_location.x) * 180 / math.pi
    angle_diff = curr_angle - new_angle

    if angle_diff > 180:
        angle_diff -= 360
    elif angle_diff < -180:
        angle_diff += 360    
    steer = angle_diff / 90

    velocity = math.sqrt(curr_velocity.x * curr_velocity.x + curr_velocity.y * curr_velocity.y + curr_velocity.z * curr_velocity.z)
    throttle = 1 if velocity < 9 else 0 # 속도가 9m/s를 넘어가지 않게 한다.

    print(f"\tvelocity={velocity:.1f} curr_loc={curr_location.x:.1f},{curr_location.y:.1f} linear_ref={distance:.1f} next_point={next_point.x:.1f}, {next_point.y:.1f} steering={steer:.1f}(curr_angle={curr_angle:.1f}, new_angle={new_angle:.1f})")
    return carla.VehicleControl(throttle, steer, 0.0, manual_gear_shift=True, gear=1) #1단으로 달린다.


def write_frame(filename, car_tf: carla.Transform, lidar : carla.LidarMeasurement):
    dict = {}
    dict['carpose'] = {
        'location': [car_tf.location.x, car_tf.location.y, car_tf.location.z],
        'rotation': [car_tf.rotation.roll, car_tf.rotation.pitch, car_tf.rotation.yaw]
    }
    dict['carposeMatrix'] = tf2matrix4list(car_tf)
    dict['lidar'] = base64.b64encode(lidar.raw_data).decode("utf-8")
    f = open(filename, "w")
    f.write(json.dumps(dict))
    f.close()


def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)

        load_world_if_needed(client, "/Game/Carla/Maps/Town01")
 
        world = client.get_world()
        world.set_weather(carla.WeatherParameters(cloudiness=20, sun_altitude_angle=45))
        #world.apply_settings(carla.WorldSettings(True, False, 1.0/30))
        map = world.get_map()

        start_tf = carla.Transform(carla.Location(x=230, y=55, z=0.1), carla.Rotation(0, 180, 0))
        start_wp = map.get_waypoint(start_tf.location)

        #end_loc = carla.Location(x=240, y=55, z=0)
        #waypoints = find_waypoins(start_wp, [10, 172, 25, 32, 2, 88, 21, 188, 22, 158, 4, 141, 17, 114, 10], 1, end_loc)

        end_loc = carla.Location(x=168, y=27, z=0)
        waypoints = find_waypoins(start_wp, [10, 172, 25], 1, end_loc)

        print('waypoint count ', len(waypoints))
        route_line = LineString([(wp.transform.location.x, wp.transform.location.y) for wp in waypoints])


        blueprint_library = world.get_blueprint_library()
        bp = blueprint_library.find('vehicle.jeep.wrangler_rubicon')

        vehicle = world.spawn_actor(bp, start_tf)
        print('created %s' % vehicle.type_id)

        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_sensors = [make_sensor(world, vehicle, camera_bp, config[0], config[1]) for config in CAMERA_CONFIGS]

        lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('range', str(200))
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('rotation_frequency', str(10))
        lidar_bp.set_attribute('points_per_second', str(10*32*360*4)) #(44841, 3)

        lidar_sensor = world.spawn_actor(
            lidar_bp,
            carla.Transform(carla.Location(x=1.5, y=0, z=2.4)),
            attach_to=vehicle)

        print('===============')
        print('physics_control')
        print(vehicle.get_physics_control())

        #vehicle.set_velocity(carla.Vector3D(-10, 0, 0)) # 초기 속도를 지정할 수 있다.
        start_time = time.process_time()
        frame = 0
        with CarlaSyncMode(world, camera_sensors[0], camera_sensors[1], camera_sensors[2], camera_sensors[3], camera_sensors[4], camera_sensors[5], camera_sensors[6], camera_sensors[7], lidar_sensor, fps=10) as sync_mode:
            while True:
                curr_tf = vehicle.get_transform()
                curr_location = vehicle.get_location()
                curr_velocity = vehicle.get_velocity()
                waypoint = map.get_waypoint(curr_location)
                vehicle.apply_control(my_control(curr_tf, curr_velocity, route_line))

                t1 = time.process_time()

                snapshot, i0, i1, i2, i3, i4, i5, i6, i7, pointcloud = sync_mode.tick(timeout=2.0)
                t2 = time.process_time()

                images = [i0, i1, i2, i3, i4, i5, i6, i7]
                print(f"frame={frame}, game_frame={snapshot.frame} road_id={waypoint.road_id}")
                for i in range(8):
                    images[i].save_to_disk("_out/%05d_camera%d.png" % (frame, i))

                t3 = time.process_time()
                pointcloud.save_to_disk("_out/%05d_lidar.ply" % (frame))
                #print(type(base64.encodebytes(pointcloud.raw_data)))

                write_frame('_out/%05d_frame.json' % frame, vehicle.get_transform(), pointcloud)
                t4 = time.process_time()

                print(f"tick={t2-t1} camera={t3-t2} frame={t4-t3}")
                #for pt in pointcloud:
                #    print(pt)
                #print('len(pointcloud)', len(pointcloud))
                #array = np.frombuffer(pointcloud.raw_data, dtype=np.dtype("float32"))
                #xyz = np.reshape(array, (-1, 3))
                #print(xyz.shape)

                spectator_tf = carla.Transform(carla.Location(curr_location.x, curr_location.y, curr_location.z+2.5), curr_tf.rotation)
                world.get_spectator().set_transform(spectator_tf)
                frame += 1

                # 탈출조건
                if curr_location.distance(end_loc) < 10: break

        print(f"success elapsed_time={time.process_time() - start_time}")

    finally:
        for camera_sensor in camera_sensors:
            camera_sensor.destroy()
        lidar_sensor.destroy()

        print('destroying vehicle')
        vehicle.destroy()

        # synchronous_mode를 해제한다.
        world.apply_settings(carla.WorldSettings(False))
        print('done.')


if __name__ == '__main__':
    main()
