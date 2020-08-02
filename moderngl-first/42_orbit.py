import math
import moderngl
import numpy as np
from pyrr import Matrix44
from ported._example import Example


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
    uniform sampler2D Texture;
    in vec3 v_vert;
    in vec3 v_norm;
    in vec2 v_text;
    out vec4 f_color;
    void main() {
        float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
        f_color = vec4(texture(Texture, v_text).rgb * lum, 1.0);
    }
'''


class CrateExample(Example):
    title = "Crate"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.mvp = self.prog['Mvp']
        self.light = self.prog['Light']

        self.scene = self.load_scene('crate.obj')
        self.vao = self.scene.root_nodes[0].mesh.vao.instance(self.prog)
        self.texture = self.load_texture_2d('crate.png')

        self.angleX = 0
        self.angleY = 3.14 / 6
        #self.lastX;
        #self.lastY;

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        camera_pos = np.array([np.cos(self.angleY)*np.cos(self.angleX), np.sin(self.angleX), np.sin(self.angleY)]) * 3

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0)

        lookat = Matrix44.look_at(
            tuple(camera_pos),  # eye
            (0.0, 0.0, 0.0),    # target
            (0.0, 0.0, 1.0),    # up
        )
        model = Matrix44.from_translation((0, 0, -0.5))

        self.mvp.write((proj * lookat * model).astype('f4'))
        self.light.value = tuple(camera_pos)
        self.texture.use()
        self.vao.render()


    def mouse_drag_event(self, x, y, dx, dy):
        self.angleX += dx * -0.01
        self.angleY += dy * 0.01

        #self.angleX = min(max(self.angleX, 0), 2*math.pi)
        self.angleY = min(max(self.angleY, 0), math.pi / 2)

        print("Mouse drag:", x, y, dx, dy, self.angleX, self.angleY)

    '''
    def mouse_position_event(self, x, y, dx, dy):
        print("Mouse position:", x, y, dx, dy)

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        print("Mouse wheel:", x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        #self.lastX = x
        #self.lastY = y
        print("Mouse button {} pressed at {}, {}".format(button, x, y))

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))
    '''

if __name__ == '__main__':
    CrateExample.run()