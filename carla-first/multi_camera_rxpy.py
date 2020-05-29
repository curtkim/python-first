import carla
import random
import time
import threading

import numpy as np
from PIL import Image

import pygame

import rx
from rx import operators as ops
from rx.scheduler.mainloop import PyGameScheduler


#WIDTH, HEIGHT = pygame.display.get_surface().get_size()
#WIDTH = 1920 #*2
#HEIGHT = 1200 #*2

WIDTH = 2560
HEIGHT = 1440

UNIT_WIDTH = int(WIDTH / 3)
UNIT_HEIGHT = int(HEIGHT / 3)

GRID_ORIGINS = [
    (UNIT_WIDTH, 0),
    (2*UNIT_WIDTH, 0),
    (2*UNIT_WIDTH, UNIT_HEIGHT),
    (2*UNIT_WIDTH, 2*UNIT_HEIGHT),
    (UNIT_WIDTH, 2*UNIT_HEIGHT),
    (0, 2*UNIT_HEIGHT),
    (0, UNIT_HEIGHT),
    (0, 0)
]

CAMERA_CONFIGS = [
    # [tranform, fov]
    [carla.Transform(carla.Location(x=1.5, y=0, z=2.4), carla.Rotation(yaw=0)), 120],
    [carla.Transform(carla.Location(x=1.5, y=0.1, z=2.4), carla.Rotation(yaw=0)), 90],
    [carla.Transform(carla.Location(x=0, y=1.1, z=2.4), carla.Rotation(yaw=45)), 90],
    [carla.Transform(carla.Location(x=1.0, y=1.1, z=1), carla.Rotation(yaw=135)), 120],
    [carla.Transform(carla.Location(x=-1.5, y=0, z=2.4), carla.Rotation(yaw=180)), 120],
    [carla.Transform(carla.Location(x=1.0, y=-1.1, z=1), carla.Rotation(yaw=225)), 120],
    [carla.Transform(carla.Location(x=0, y=-1.1, z=2.4), carla.Rotation(yaw=315)), 90],
    [carla.Transform(carla.Location(x=1.5, y=-0.1, z=2.4), carla.Rotation(yaw=0)), 45],
]

def make_sensor(world, vehicle, rgb_bp, tf, fov):
    rgb_bp.set_attribute('image_size_x', str(UNIT_WIDTH))
    rgb_bp.set_attribute('image_size_y', str(UNIT_HEIGHT))
    rgb_bp.set_attribute('fov', str(fov))
    rgb_bp.set_attribute('sensor_tick', '0.033')
    return world.spawn_actor(rgb_bp, tf, attach_to=vehicle)


def image_carla2numpy(image):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    return pygame.surfarray.make_surface(array.swapaxes(0, 1))


def from_sensor(sensor, idx):
    def subscribe(observer, scheduler):
        def callback(image):
            #print('from_sensor', idx, threading.get_ident())
            observer.on_next(image_carla2numpy(image))
        sensor.listen(callback)

    return rx.create(subscribe)


def main():

    try:
        pygame.init()
        pygame.font.init()
        pygame_scheduler = PyGameScheduler(pygame)

        display = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF)


        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)
        client.load_world("/Game/Carla/Maps/Town10HD")

        world = client.get_world()

        blueprint_library = world.get_blueprint_library()
        bp = random.choice(blueprint_library.filter('vehicle'))
        rgb_bp = blueprint_library.find('sensor.camera.rgb')

        spawn_points = world.get_map().get_spawn_points()
        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()

        vehicle = world.try_spawn_actor(bp, spawn_point)

        print('created %s' % vehicle.type_id)
        vehicle.set_autopilot(True)

        sensors = [make_sensor(world, vehicle, rgb_bp, config[0], config[1]) for config in CAMERA_CONFIGS]
        image_obs = [from_sensor(sensor, idx) for idx, sensor in enumerate(sensors)]

        def grid_draw(params):
            frame = params[0]
            images = params[1:]
            for idx, image in enumerate(images):
                display.blit(image, GRID_ORIGINS[idx])
            pygame.display.flip()

        rx.interval(0.033).pipe(
            ops.with_latest_from(*image_obs),
            ops.observe_on(pygame_scheduler),
        ).subscribe(grid_draw)

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick_busy_loop(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame_scheduler.run()


    finally:
        print('finally')
        for sensor in sensors:
            sensor.stop()
            sensor.destroy()
        vehicle.destroy()

        pygame.quit()
        print('done')


if __name__ == '__main__':
    main()
    print('last sleep')
    time.sleep(2)
