import carla
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from omegaconf import DictConfig
from omegaconf import OmegaConf

from carlax.carla_sync_mode import CarlaSyncMode
from carlax.pid_controller import VehiclePIDController
from carlax.common import remove_all_actors, load_world_if_needed, destroy_actors, get_speed
from carlax.npc_planner import create_start_end_npc_planner, create_speed_points_npc_planner

BASE_HEIGHT = 0.5
FPS = 20 # frame per second

def show_results(df):

    frame = np.arange(len(df)) / FPS

    fig, ax = plt.subplots(5, figsize=(5, 2.5*5))

    ax[0].title.set_text("xy")
    ax[0].invert_yaxis()
    ax[0].plot(df['x'], df['y'])
    for i in range(0, len(df), FPS):
        ax[0].annotate(int(i/FPS), (df['x'][i], df['y'][i]))

    ax[1].title.set_text("speed")
    ax[1].plot(frame, df['speed'])

    ax[2].title.set_text("steer")
    ax[2].plot(frame, df['steer'])

    ax[3].title.set_text("throttle")
    ax[3].plot(frame, df['throttle'])

    ax[4].title.set_text("brake")
    ax[4].plot(frame, df['brake'])

    fig.tight_layout()
    plt.show()


def main(cfg: DictConfig):
    start_time = time.process_time()

    carla_cfg = cfg.client
    client = carla.Client(carla_cfg.host, carla_cfg.port)
    client.set_timeout(carla_cfg.timeout)

    load_world_if_needed(client, "/Game/Carla/Maps/Town01_Opt")
    #client.load_world("/Game/Carla/Maps/Town01_Opt")

    world = client.get_world()
    remove_all_actors(world)
    world.unload_map_layer(carla.MapLayer.All)
    carla_map = world.get_map()
    time.sleep(1)

    blueprint_library = world.get_blueprint_library()

    vehicle_bp = blueprint_library.find('vehicle.lincoln.mkz2017')

    points = [
        [180, 59, 0],
        [150, 59, 50],
        [120, 55.5, 50],
        [100, 55.5, 20],
        [ 90, 55.5, 10],
    ]

    start_loc = carla.Location(x=points[0][0], y=points[0][1], z=BASE_HEIGHT)
    #end_loc = carla.Location(x=120, y=-2, z=0)
    start_rotation = carla_map.get_waypoint(start_loc).transform.rotation
    print(start_rotation)

    vehicle = world.spawn_actor(vehicle_bp, carla.Transform(start_loc, carla.Rotation(pitch=0, yaw=180, roll=0)))
    #vehicle2 = world.spawn_actor(vehicle_bp, carla.Transform(start_loc, start_rotation))

    pid_cfg = cfg.vehicle_pid_controller
    vehicle_controller = VehiclePIDController(vehicle,
                                                    args_lateral=pid_cfg.args_lateral,
                                                    args_longitudinal=pid_cfg.args_longitudinal,
                                                    offset=pid_cfg.offset,
                                                    max_throttle=pid_cfg.max_throttle,
                                                    max_brake=pid_cfg.max_brake,
                                                    max_steering=pid_cfg.max_steer)

    #npc_planner = create_start_end_npc_planner(carla_map, start_loc, end_loc, 10, vehicle_controller)
    end_loc = carla.Location(points[-1][0], points[-1][1], 0)
    npc_planner = create_speed_points_npc_planner(points[1:], vehicle_controller)

    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', str(800))
    camera_bp.set_attribute('image_size_y', str(600))
    camera_bp.set_attribute('fov', str(90))
    camera_bp.set_attribute('sensor_tick', '0.033')
    camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=0, y=0, z=2.0), carla.Rotation(yaw=0)), attach_to=vehicle)

    '''
    collision_bp = world.get_blueprint_library().find('sensor.other.collision')
    collision_sensor = world.spawn_actor(collision_bp, carla.Transform(carla.Location(x=0, y=0, z=0)), attach_to=vehicle)

    def collision_callback(measurement):
        print(
            f"""coll frame={measurement.frame} transform={measurement.transform} actor={measurement.actor} other_actor={measurement.other_actor}""")

    collision_sensor.listen(collision_callback)
    '''

    spectator_tf = carla.Transform(carla.Location(x=150, y=55, z=30), carla.Rotation(-45, 180, 0))
    world.get_spectator().set_transform(spectator_tf)


    results = []
    frame = 0
    with CarlaSyncMode(world, camera, fps=FPS) as sync_mode:
        # vehicle spawn후에 안정화를 위해 1초를 보낸다.
        for i in range(FPS):
            world.tick()

        while True:
            #curr_tf = vehicle.get_transform()
            curr_location = vehicle.get_location()
            control = npc_planner(curr_location)
            vehicle.apply_control(control)
            results.append([control.steer, control.throttle, control.brake,
                            curr_location.x, curr_location.y, curr_location.z,
                            get_speed(vehicle)])

            #world.tick()
            snapshot, image = sync_mode.tick(timeout=2.0)
            #image.save_to_disk("_out/%05d_camera.png" % (frame))

            #print(frame, snapshot.frame, curr_location, vehicle.get_velocity(), control)
            #spectator_tf = carla.Transform(carla.Location(curr_location.x, curr_location.y, curr_location.z + 2.5),
            #                               curr_tf.rotation)
            #world.get_spectator().set_transform(spectator_tf)
            frame += 1

            # 탈출조건
            if curr_location.distance(end_loc) < 3 : break

    time.sleep(1)
    print("elapse time", time.process_time() - start_time, "frame", frame)

    df = pd.DataFrame(np.array(results), columns=['steer', 'throttle', 'brake', 'x', 'y', 'z', 'speed'])
    show_results(df)

    destroy_actors(vehicle, camera)



if __name__ == '__main__':
    conf = OmegaConf.create({
        "client": {
            "host": "localhost",
            "port": 2000,
            "timeout": 5.0
        },
        "vehicle_pid_controller": {
            "args_lateral": {
                'K_P': 0.8,
                'K_D': 0,
                'K_I': 0.001,
                'dt': 1.0 / 20.0
            },
            "args_longitudinal": {
                'K_P': 1.0,
                'K_D': 0,
                'K_I': 0.05,
                'dt': 1.0 / 20.0
            },
            "offset": 0,
            "max_throttle": 0.75,
            "max_brake": 0.3,
            "max_steer": 0.8,
        },
    })

    main(conf)
