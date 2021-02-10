import carla
import random
import time


def main():
    actor_list = []

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        world = client.get_world()

        blueprint_library = world.get_blueprint_library()
        bp = random.choice(blueprint_library.filter('vehicle'))
        if bp.has_attribute('color'):
            color = random.choice(bp.get_attribute('color').recommended_values)
            bp.set_attribute('color', color)

        transform = carla.Transform(carla.Location(x=40, y=-3.2), carla.Rotation())

        vehicle = world.spawn_actor(bp, transform)
        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)

        cc = carla.ColorConverter

        '''
        tfs = [carla.Transform(carla.Location(x=1.5, y=0, z=2.4), carla.Rotation(yaw=0)),
               carla.Transform(carla.Location(x=0, y=1, z=2.4), carla.Rotation(yaw=90)),
               carla.Transform(carla.Location(x=-1.5, y=0, z=2.4), carla.Rotation(yaw=180)),
               carla.Transform(carla.Location(x=0, y=-1, z=2.4), carla.Rotation(yaw=270))]
        '''
        tfs = [carla.Transform(carla.Location(x=1.5, y=0, z=2.4), carla.Rotation(yaw=180))]

        def make_listener(format, idx):
            def callback(image):
                image.save_to_disk(format % (idx, image.frame))
            return callback

        for i, tf in enumerate(tfs):
            rgb_bp = blueprint_library.find('sensor.camera.rgb')
            rgb_bp.set_attribute('image_size_x', str(1200))
            rgb_bp.set_attribute('image_size_y', str(800))
            rgb_camera = world.spawn_actor(rgb_bp, tf, attach_to=vehicle)
            actor_list.append(rgb_camera)
            print('created %s' % rgb_camera.type_id)
            rgb_camera.listen(make_listener('_out/rgb_%d_%06d.jpg', i))

            depth_bp = blueprint_library.find('sensor.camera.depth')
            depth_camera = world.spawn_actor(depth_bp, tf, attach_to=vehicle)
            actor_list.append(depth_camera)
            print('created %s' % depth_camera.type_id)
            depth_camera.listen(make_listener('_out/depth_%d_%06d.png', i))

        """
        lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('range', str(200))
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('rotation_frequency', str(10))
        lidar_bp.set_attribute('points_per_second', str(360*10*10*32))
        lidar_sensor = world.spawn_actor(lidar_bp, carla.Transform(carla.Location(x=1.5, y=0, z=2.4)), attach_to=vehicle)
        actor_list.append(lidar_sensor)
        print('created %s' % lidar_sensor.type_id)
        def lidar_callback(measurement):
            measurement.save_to_disk('_out/pc_%06d.ply' % measurement.frame)
        lidar_sensor.listen(lidar_callback)
        """

        time.sleep(20)

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
