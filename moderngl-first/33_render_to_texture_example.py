import os

import moderngl
import numpy as np
from PIL import Image
from pyrr import Matrix44

from ported._example import Example


def local(*path):
    return os.path.join(os.path.dirname(__file__), *path)


vertex_shader = '''
    #version 330
    uniform mat4 Mvp;

    in vec3 in_position;
    in vec3 in_normal;
    in vec2 in_texcoord_0;

    out vec3 v_vert;
    out vec3 v_norm;
    out vec2 v_text;

    void main() {
        gl_Position = Mvp * vec4(in_position, 1.0);
        v_vert = in_position;
        v_norm = in_normal;
        v_text = in_texcoord_0;
    }
'''
fragment_shader = '''
    #version 330

    uniform vec3 Light;
    uniform vec3 Color;
    uniform bool UseTexture;
    uniform sampler2D Texture;

    in vec3 v_vert;
    in vec3 v_norm;
    in vec2 v_text;

    out vec4 f_color;

    void main() {
        float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
        if (UseTexture) {
            f_color = vec4(texture(Texture, v_text).rgb * lum, 1.0);
        } else {
            f_color = vec4(Color * lum, 1.0);
        }
    }
'''


class RenderToTexture(Example):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.mvp = self.prog['Mvp']
        self.light = self.prog['Light']
        self.color = self.prog['Color']
        self.use_texture = self.prog['UseTexture']

        # Load obj files
        self.scene_ground = self.load_scene('scene-1-ground.obj')
        self.scene_grass = self.load_scene('scene-1-grass.obj')
        self.scene_billboard = self.load_scene('scene-1-billboard.obj')
        self.scene_holder = self.load_scene('scene-1-billboard-holder.obj')
        self.scene_image = self.load_scene('scene-1-billboard-image.obj')

        # Extract the VAOs from the scene
        self.vao_ground = self.scene_ground.root_nodes[0].mesh.vao.instance(self.prog)
        self.vao_grass = self.scene_grass.root_nodes[0].mesh.vao.instance(self.prog)
        self.vao_billboard = self.scene_billboard.root_nodes[0].mesh.vao.instance(self.prog)
        self.vao_holder = self.scene_holder.root_nodes[0].mesh.vao.instance(self.prog)
        self.vao_image = self.scene_image.root_nodes[0].mesh.vao.instance(self.prog)

        # texture on billboard
        self.texture1 = self.load_texture_2d('infographic-1.jpg')

        self.texture2 = self.ctx.texture(self.window_size, 3)
        depth_attachment = self.ctx.depth_renderbuffer(self.window_size)
        self.fbo = self.ctx.framebuffer(self.texture2, depth_attachment)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (47.697, -8.147, 24.498),
            (0.0, 0.0, 8.0),
            (0.0, 0.0, 1.0),
        )

        rotate = Matrix44.from_z_rotation(np.sin(time) * 0.5 + 0.2)

        for mode in ['render_to_texture', 'render_to_window']:
            if mode == 'render_to_texture':
                self.fbo.clear(1.0, 1.0, 1.0)
                self.fbo.use()
            else:
                self.ctx.screen.use()

            self.use_texture.value = False

            self.light.value = (67.69, -8.14, 52.49)
            self.mvp.write((proj * lookat * rotate).astype('f4').tobytes())

            self.color.value = (0.67, 0.49, 0.29)
            self.vao_ground.render()

            self.color.value = (0.46, 0.67, 0.29)
            self.vao_grass.render()

            self.color.value = (1.0, 1.0, 1.0)
            self.vao_billboard.render()

            self.color.value = (0.2, 0.2, 0.2)
            self.vao_holder.render()

            self.use_texture.value = True

            if mode == 'render_to_texture':
                self.texture1.use()
            else:
                self.texture2.use()

            self.vao_image.render()

if __name__ == '__main__':
    RenderToTexture.run()
