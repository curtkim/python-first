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
import math
from shapely.geometry import Point, LineString


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


def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        load_world_if_needed(client, "/Game/Carla/Maps/Town01")
 
        world = client.get_world()        
        world.apply_settings(carla.WorldSettings(True, False, 1.0/30))
        map = world.get_map()

        start_tf = carla.Transform(carla.Location(x=230, y=55, z=0.1), carla.Rotation(0, 180, 0))
        start_wp = map.get_waypoint(start_tf.location)
        end_loc = carla.Location(x=240, y=55, z=0)
                                                                           
        waypoints = find_waypoins(start_wp, [10, 172, 25, 32, 2, 88, 21, 188, 22, 158, 4, 141, 17, 114, 10], 1, end_loc)
        print('waypoint count ', len(waypoints))
        route_line = LineString([(wp.transform.location.x, wp.transform.location.y) for wp in waypoints])


        blueprint_library = world.get_blueprint_library()
        bp = blueprint_library.find('vehicle.jeep.wrangler_rubicon')

        vehicle = world.spawn_actor(bp, start_tf)
        print('created %s' % vehicle.type_id)

        print('===============')
        print('physics_control')
        print(vehicle.get_physics_control())

        #vehicle.set_velocity(carla.Vector3D(-10, 0, 0)) # 초기 속도를 지정할 수 있다.
        while True:
            curr_tf = vehicle.get_transform()
            curr_location = vehicle.get_location()
            curr_velocity = vehicle.get_velocity()
            waypoint = map.get_waypoint(curr_location)
            vehicle.apply_control(my_control(curr_tf, curr_velocity, route_line))
            frame = world.tick()
            print(f"frame={frame}, road_id={waypoint.road_id}")

            spectator_tf = carla.Transform(carla.Location(curr_location.x, curr_location.y, curr_location.z+2.5), curr_tf.rotation)
            world.get_spectator().set_transform(spectator_tf)

            if curr_location.distance(end_loc) < 3: break

        print("success")

    finally:
        print('destroying vehicle')
        vehicle.destroy()

        # synchronous_mode를 해제한다.
        world.apply_settings(carla.WorldSettings(False))
        print('done.')


if __name__ == '__main__':
    main()
