import numpy as np

from ported._example import Example

vertex_shader = '''
    #version 330
    in vec2 vert;
    
    uniform vec2 scale;
    uniform float rotation;
    
    void main() {
        mat2 rot = mat2(
            cos(rotation), sin(rotation),
            -sin(rotation), cos(rotation)
        );
        gl_Position = vec4((rot * vert) * scale, 0.0, 1.0);
    }
'''
fragment_shader = '''
    #version 330
    out vec4 color;
    void main() {
        color = vec4(0.3, 0.5, 1.0, 1.0);
    }
'''


class UniformsAndAttributes(Example):
    gl_version = (3, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.scale = self.prog['scale']
        self.rotation = self.prog['rotation']

        self.scale.value = (self.wnd.width / self.wnd.height * 0.75, 0.25)

        vertices = np.array([
            1.0, 0.0,
            -0.5, 0.86,
            -0.5, -0.86,
        ], dtype='f4')

        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')

    def render(self, time: float, frame_time: float):
        sin_scale = np.sin(np.deg2rad(time * 60))
        self.scale.value = (sin_scale * 0.75, 0.75)
        self.rotation.value = time

        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render()


if __name__ == '__main__':
    UniformsAndAttributes.run()