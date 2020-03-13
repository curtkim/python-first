import struct

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

        in vec2 in_vert;

        in vec3 in_color;
        out vec3 v_color;    // Goes to the fragment shader

        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_color = in_color;
        }
    ''',
    fragment_shader='''
        #version 330

        in vec3 v_color;
        out vec4 f_color;

        void main() {
            // We're not interested in changing the alpha value
            f_color = vec4(v_color, 1.0);
        }
    ''',
)

# Point coordinates are put followed by the vec3 color values
vertices = np.array([
    # x, y, red, green, blue
    0.0, 0.8, 1.0, 0.0, 0.0,
    -0.6, -0.8, 0.0, 1.0, 0.0,
    0.6, -0.8, 0.0, 0.0, 1.0,
])

vbo = ctx.buffer(vertices.astype('f4').tobytes())

# We control the 'in_vert' and `in_color' variables
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.9, 0.9, 0.9)
    vao.render()

    pygame.display.flip()
    pygame.time.wait(6)
