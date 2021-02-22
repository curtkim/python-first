# 목표
- 다시 실행했을때 같은 결과가 나와야 한다.
- 시나리오를 기술하기 쉬워야 한다.
- 하나의 command line으로 실행되어야 한다.
- 모든 사람의 컴퓨터에서 동일하게 실행되어야 한다.(쉬운 설치)

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

# 실행 옵션
- [input] scenario only
- [output] interactive
- [output] make video

# c++ interface

    std::tuple<ControlOutput, PlannerState> Plan(EgoState ego, ObstacleList obstacles, WaypointList waypoints, PlannerState state);
    
# Continuous Test
1. github commit 
2. docker build(in docker hub)
3. notify my desktop
5. docker pull 
6. run test by docker-compose 
7. upload? report and messenger notify

# docker 

    docker run --net=host --gpus all --volume /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=unix$DISPLAY --entrypoint /home/carla/CarlaUE4.sh carlasim/carla:0.9.11 -opengl
    sh: 1: xdg-user-dir: not found