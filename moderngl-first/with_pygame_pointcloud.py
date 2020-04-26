import numpy as np
import moderngl
import pygame
from pygame.locals import DOUBLEBUF, OPENGL

import open3d as o3d
from camera import Camera


pygame.init()
pygame.display.set_mode((1600, 1200), DOUBLEBUF | OPENGL)

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

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

pcd_load = o3d.io.read_point_cloud("./pc_000247.ply")
xyz_load = np.asarray(pcd_load.points)

vbo = ctx.buffer(xyz_load.astype('f4').tobytes())
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')

camera = Camera(16/9)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                camera.move_forward()
            elif event.key == pygame.K_s:
                camera.move_backwards()

    ctx.clear(1., 1., 1.)
    mvp.write((camera.mat_projection * camera.mat_lookat).astype('f4').tobytes())
    vao.render(moderngl.POINTS)

    pygame.display.flip()
    pygame.time.wait(6)
