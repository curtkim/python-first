# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys
import threading

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================


import carla

from carla import ColorConverter as cc

import argparse
import collections
import datetime
import logging
import math
import random
import re
import weakref

try:
    import pygame
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')


# ==============================================================================
# -- game_loop() ---------------------------------------------------------------
# ==============================================================================
surface = None

def game_loop(args):
    pygame.init()
    pygame.font.init()
    world = None
    actor_list = []    

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(2.0)

        #with open('Town01.xodr', 'r') as xodr_file:
        #    xodr = xodr_file.read()
        #    client.generate_opendrive_world(xodr)

        world = client.get_world()
        map = world.get_map()

        blueprint_library = world.get_blueprint_library()
        bp = blueprint_library.find('vehicle.jeep.wrangler_rubicon')

        spawn_points = map.get_spawn_points()
        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        vehicle = world.try_spawn_actor(bp, spawn_point)
        vehicle.set_autopilot(True)
        actor_list.append(vehicle)

        
        def callback(image):
            global surface
            image.convert(cc.Raw)
            array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (image.height, image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))            
            print(f"{threading.get_ident()}")

        rgb_bp = blueprint_library.find('sensor.camera.rgb')
        rgb_bp.set_attribute('image_size_x', str(args.width))
        rgb_bp.set_attribute('image_size_y', str(args.height))
        rgb_bp.set_attribute('fov', str(90))
        rgb_bp.set_attribute('sensor_tick', '0.033')

        tf = carla.Transform(carla.Location(x=1.5, y=0, z=2.4), carla.Rotation(yaw=0))
        rgb_camera = world.spawn_actor(rgb_bp, tf, attach_to=vehicle)
        actor_list.append(rgb_camera)
        print('created %s' % (rgb_camera.type_id))
        rgb_camera.listen(callback)


        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        clock = pygame.time.Clock()
        while True:
            clock.tick_busy_loop(60)
            if surface:
                display.blit(surface, (0,0))
            pygame.display.flip()

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

        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    argparser = argparse.ArgumentParser(
        description='CARLA Manual Control Client')
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-a', '--autopilot',
        action='store_true',
        help='enable autopilot')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1500x1200',
        help='window resolution (default: 1500x1200)')
    argparser.add_argument(
        '--filter',
        metavar='PATTERN',
        default='vehicle.*',
        help='actor filter (default: "vehicle.*")')
    argparser.add_argument(
        '--rolename',
        metavar='NAME',
        default='hero',
        help='actor role name (default: "hero")')
    argparser.add_argument(
        '--gamma',
        default=2.2,
        type=float,
        help='Gamma correction of the camera (default: 2.2)')
    args = argparser.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:

        game_loop(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':

    main()