def remove_all_actors(world):
    actors = world.get_actors()
    for actor in actors:
        one_depth_type = actor.type_id.split(".")[0]
        if one_depth_type in ['vehicle', 'walker']:
            print('remove', actor.type_id, actor.id)
            actor.destroy()

def load_world_if_needed(client, map_name):
    if not map_name.endswith(client.get_world().get_map().name):
        client.load_world(map_name)
    else:
        print('current map is already ', map_name)

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
            raise Exception("filtered count is not 1")
        curr = filtered[0]
        print(road_ids, curr.road_id, curr.s)
        #print_waypoint(curr)
        results.append(curr)
        if road_ids.index(curr.road_id) == 1:
            road_idx += 1
            road_ids = trace_road_ids[road_idx:road_idx+2]

    return results
