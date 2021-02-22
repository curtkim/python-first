import carla
import time

from omegaconf import DictConfig
from omegaconf import OmegaConf

from carlax.carla_sync_mode import CarlaSyncMode
from carlax.pid_controller import VehiclePIDController
from carlax.common import remove_all_actors, load_world_if_needed, destroy_actors
from carlax.npc_planner import create_start_end_npc_planner, create_speed_points_npc_planner


def main(cfg: DictConfig):

    try:
        carla_cfg = cfg.client
        client = carla.Client(carla_cfg.host, carla_cfg.port)
        client.set_timeout(carla_cfg.timeout)

        load_world_if_needed(client, "/Game/Carla/Maps/Town01")

        world = client.get_world()
        remove_all_actors(world)
        world.unload_map_layer(carla.MapLayer.All)
        carla_map = world.get_map()

        blueprint_library = world.get_blueprint_library()

        vehicle_bp = blueprint_library.find('vehicle.lincoln.mkz2017')


        start_loc = carla.Location(x=180, y=55, z=0.5)
        end_loc = carla.Location(x=120, y=-2, z=0)
        start_rotation = carla_map.get_waypoint(start_loc).transform.rotation

        vehicle = world.spawn_actor(vehicle_bp, carla.Transform(start_loc, start_rotation))

        pid_cfg = cfg.vehicle_pid_controller
        vehicle_controller = VehiclePIDController(vehicle,
                                                        args_lateral=pid_cfg.args_lateral,
                                                        args_longitudinal=pid_cfg.args_longitudinal,
                                                        offset=pid_cfg.offset,
                                                        max_throttle=pid_cfg.max_throttle,
                                                        max_brake=pid_cfg.max_brake,
                                                        max_steering=pid_cfg.max_steer)

        #npc_planner = create_start_end_npc_planner(carla_map, start_loc, end_loc, 10, vehicle_controller)
        points = [
            [179, 55, 1],
            [160, 57, 20],
            [150, 58, 20],
            [140, 57, 20],
            [120, 55, 10],
            [100, 55, 5],
        ]
        end_loc = carla.Location(x=100, y=55, z=0)
        npc_planner = create_speed_points_npc_planner(points, vehicle_controller)

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
                control = npc_planner(curr_location)
                vehicle.apply_control(control)

                snapshot, image = sync_mode.tick(timeout=2.0)
                #image.save_to_disk("_out/%05d_camera.png" % (frame))

                print(frame, curr_location, vehicle.get_velocity(), control)
                spectator_tf = carla.Transform(carla.Location(curr_location.x, curr_location.y, curr_location.z + 2.5),
                                               curr_tf.rotation)
                world.get_spectator().set_transform(spectator_tf)
                frame += 1

                # 탈출조건
                if curr_location.distance(end_loc) < 3: break

        time.sleep(1)

    finally:
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
