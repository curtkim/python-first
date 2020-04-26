# carla - moderngl - pygame

import glob
import os
import sys

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

import rx
from rx import operators as ops
from rx.scheduler.mainloop import PyGameScheduler

import moderngl
from pyrr import Matrix44, Quaternion, Vector3, vector

from camera import Camera

try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_c
    from pygame.locals import K_g
    from pygame.locals import K_d
    from pygame.locals import K_h
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_w
    from pygame.locals import K_l
    from pygame.locals import K_i
    from pygame.locals import K_z
    from pygame.locals import K_x
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')


def lidar_carla2numpy(measurement):
    array = np.frombuffer(measurement.raw_data, dtype=np.dtype("float32"))
    return np.reshape(array, (-1, 3))


def from_sensor(sensor):
    def subscribe(observer, scheduler):
        def callback(measurement):
            #print('from_sensor', idx, threading.get_ident())
            observer.on_next(lidar_carla2numpy(measurement))
        sensor.listen(callback)

    return rx.create(subscribe)



# ==============================================================================
# -- game_loop() ---------------------------------------------------------------
# ==============================================================================

def game_loop(args):
    pygame.init()
    pygame.font.init()

    scheduler = PyGameScheduler(pygame)

    world = None
    actor_list = []

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(2.0)
        world = client.get_world()
        map = world.get_map()

        blueprint_library = world.get_blueprint_library()
        bp = blueprint_library.find('vehicle.jeep.wrangler_rubicon')

        spawn_points = map.get_spawn_points()
        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        vehicle = world.try_spawn_actor(bp, spawn_point)
        vehicle.set_autopilot(True)
        actor_list.append(vehicle)


        lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('range', str(200))
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('rotation_frequency', str(10))
        lidar_bp.set_attribute('points_per_second', str(360*10*10*32))
        lidar_sensor = world.spawn_actor(lidar_bp, carla.Transform(carla.Location(x=1.5, y=0, z=2.4)), attach_to=vehicle)
        actor_list.append(lidar_sensor)
        print('created %s' % lidar_sensor.type_id)


        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.OPENGL | pygame.DOUBLEBUF)

        lidar_obs = from_sensor(lidar_sensor)

        ctx = moderngl.create_context()
        prog = ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 Mvp;

                in vec3 in_vert;
                out vec4 frag_color;
                void main() {
                    frag_color = mix(vec4(0.0, 0.0, 1.0, 1.0), vec4(0.0, 1.0, 0.0, 1.0), abs(sin(in_vert.z)));
                    gl_Position = Mvp * vec4(in_vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                in vec4 frag_color;
                out vec4 f_color;
                void main() {
                    f_color = frag_color;
                    //f_color = vec4(0.1, 0.1, 0.1, 1.0);
                }
            ''',
        )
        mvp = prog['Mvp']

        camera = Camera(args.width / args.height)


        def lidar_draw(params):
            frame = params[0]
            xyz = params[1]

            ctx.clear(1.0, 1.0, 1.0)
            ctx.enable(moderngl.DEPTH_TEST)

            vbo = ctx.buffer(xyz.astype('f4').tobytes())
            vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')
            mvp.write((camera.mat_projection * camera.mat_lookat).astype('f4').tobytes())
            vao.render(moderngl.POINTS)

            pygame.display.flip()


        rx.interval(0.033).pipe(
            ops.with_latest_from(lidar_obs),
            ops.observe_on(scheduler),
        ).subscribe(lidar_draw)

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick_busy_loop(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            scheduler.run()


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
        default='1920x1600',
        help='window resolution (default: 1920x1600)')
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