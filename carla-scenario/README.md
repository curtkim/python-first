# 시나리오 
## 1. Map
- opendrive
- lanelet

## 2. Other vehicle control
- waypoint(x, y, 속도)
- road_id list, constant target speed
- ego vehicle기준으로 behavior를 기술

## 3. Traffic Light


# 조건
- 충돌이 없다.
- waypoints를 1m buffer로 벗어나지 않았다. 
- 목적지에 도착했다.
- 시간내에 

# 시각화
- spectator, video, tensorboard?
- 속도, 스로틀, steer 그래프
- 지도

# c++ interface

    std::tuple<ControlOutput, PlannerState> Plan(EgoState ego, ObstacleList obstacles, WaypointList waypoints, PlannerState state);