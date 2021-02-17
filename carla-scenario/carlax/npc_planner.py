import carla
import math
import networkx as nx

from shapely.geometry import Point, LineString
from carlax.pid_controller import VehiclePIDController


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
            print('curr.transform.location', curr.transform.location)
            raise Exception("filtered count is not 1")

        curr = filtered[0]
        print(road_ids, curr.road_id, curr.s)
        #print_waypoint(curr)
        results.append(curr)
        if road_ids.index(curr.road_id) == 1:
            road_idx += 1
            road_ids = trace_road_ids[road_idx:road_idx+2]

    return results


def create_start_end_npc_planner(carla_map: carla.Map, start_loc: carla.Location, end_loc: carla.Location,
                                 speed: float, vehicle_pid_controller: VehiclePIDController):

    start_wp = carla_map.get_waypoint(start_loc)
    end_wp = carla_map.get_waypoint(end_loc)
    print(f"start road_id:{start_wp.road_id} land_id:{start_wp.lane_id}, end road_id:{end_wp.road_id}, land_id:{end_wp.lane_id}")

    pairs = carla_map.get_topology()
    G = nx.Graph()
    G.add_edges_from([(pair[0].road_id, pair[1].road_id) for pair in pairs])
    path = nx.shortest_path(G, start_wp.road_id, end_wp.road_id)
    print(f"path={path}")

    INTERVAL = 1
    waypoints = find_waypoins(start_wp, path, INTERVAL, end_loc)
    route_line = LineString([(wp.transform.location.x, wp.transform.location.y) for wp in waypoints])

    def fun(curr_loc: carla.Location):
        distance = route_line.project(Point(curr_loc.x, curr_loc.y))

        DELTA = 2
        next_point = route_line.interpolate(distance + DELTA)
        next_waypoint = carla_map.get_waypoint(carla.Location(next_point.x, next_point.y, 0))

        return vehicle_pid_controller.run_step(speed, next_waypoint.transform)

    return fun


def find_index_first(lst: list, predicate):
    for i, elem in enumerate(lst):
        if predicate(elem):
            return i
    return len(lst)


def rad2degree(rad: float) -> float:
    return rad * 180 / math.pi


def _create_speed_points_npc_planner_inner(points):
    route_line = LineString([pt for pt in points])
    distances = [route_line.project(Point(pt[0], pt[1], pt[2])) for pt in points]

    def fun(curr_loc: carla.Location):
        distance = route_line.project(Point(curr_loc.x, curr_loc.y))
        idx = find_index_first(distances, lambda d: d >= distance)

        target_pt = points[idx]
        yaw = 0
        if idx < len(points)-1:
            next_pt = points[idx+1]
            yaw = math.atan2(next_pt[1] - target_pt[1], next_pt[0] - target_pt[0])
        return [target_pt, rad2degree(yaw)]

    return fun


def create_speed_points_npc_planner(points, vehicle_pid_controller: VehiclePIDController):
    inner_fun = _create_speed_points_npc_planner_inner(points)

    def fun(curr_loc: carla.Location) -> carla.VehicleControl:
        [target_pt, yaw] = inner_fun(curr_loc)

        return vehicle_pid_controller.run_step(
            target_pt[2],
            carla.Transform(
                carla.Location(target_pt[0], target_pt[1], 0),
                carla.Rotation(0, yaw, 0)
            )
        )

    return fun



