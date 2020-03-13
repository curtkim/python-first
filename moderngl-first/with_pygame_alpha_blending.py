import struct

import time
import numpy as np
import moderngl
import pygame
from pygame.locals import DOUBLEBUF, OPENGL

pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

ctx = moderngl.create_context()

prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec2 vert;

        in vec4 vert_color;
        out vec4 frag_color;

        uniform vec2 scale;
        uniform float rotation;

        void main() {
            frag_color = vert_color;
            float r = rotation * (0.5 + gl_InstanceID * 0.05);
            mat2 rot = mat2(cos(r), sin(r), -sin(r), cos(r));
            gl_Position = vec4((rot * vert) * scale, 0.0, 1.0);
        }
    ''',
    fragment_shader='''
        #version 330
        in vec4 frag_color;
        out vec4 color;
        void main() {
            color = vec4(frag_color);
        }
    ''',
)

scale = prog['scale']
rotation = prog['rotation']

scale.value = (0.5, 0.5)

vertices = np.array([
    1.0, 0.0,
    1.0, 0.0, 0.0, 0.5,

    -0.5, 0.86,
    0.0, 1.0, 0.0, 0.5,

    -0.5, -0.86,
    0.0, 0.0, 1.0, 0.5,
])

vbo = ctx.buffer(vertices.astype('f4').tobytes())
vao = ctx.simple_vertex_array(prog, vbo, 'vert', 'vert_color')

start_time = time.time()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(1.0, 1.0, 1.0)
    ctx.enable(moderngl.BLEND)
    rotation.value = time.time() - start_time
    vao.render(instances=3) # gl_InstanceID

    pygame.display.flip()
    pygame.time.wait(1)
