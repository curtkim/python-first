import copy
import numpy as np
import open3d as o3d

import carla
import random
import time

# o3d를 통해서 load하고 ply로 저장
def main():
    actor_list = []

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        client.load_world("/Game/Carla/Maps/Town04")

        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        bp = random.choice(blueprint_library.filter('vehicle'))

        transform = carla.Transform(carla.Location(x=40, y=-3.2, z=1), carla.Rotation())
        vehicle = world.spawn_actor(bp, transform)
        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)

        lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('range', str(200))
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('rotation_frequency', str(10))
        lidar_bp.set_attribute('points_per_second', str(360*10*10*32))
        lidar_sensor = world.spawn_actor(lidar_bp, carla.Transform(carla.Location(x=1.5, y=0, z=2.4)), attach_to=vehicle)
        actor_list.append(lidar_sensor)
        print('created %s' % lidar_sensor.type_id)

        def lidar_callback(measurement):
            print(f"frame={measurement.frame} horizontal_angle={measurement.horizontal_angle} {measurement.get_point_count(1)} {len(measurement.raw_data)}")

            array = np.frombuffer(measurement.raw_data, dtype=np.dtype("float32"))
            xyz = np.reshape(array, (-1, 3))
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(xyz)
            o3d.io.write_point_cloud('_out/pc_%06d_o3d.ply' % measurement.frame, pcd)
            measurement.save_to_disk('_out/pc_%06d.ply' % measurement.frame)            

        lidar_sensor.listen(lidar_callback)

        time.sleep(5)

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
    print('last sleep')
    time.sleep(2)
