import numpy as np

from ported._example import Example

vertex_shader = '''
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
out vec2 TexCoord;
void main()
{
    gl_Position = vec4(aPos, 1.0);
    TexCoord = aTexCoord; // vec2(aTexCoord.x, aTexCoord.y);
}
'''
fragment_shader = '''
#version 330 core
in vec2 TexCoord;

out vec4 FragColor;
// texture sampler

uniform sampler2D texture0;
void main()
{
    FragColor = texture(texture0, TexCoord);
}
'''


class SimpleTexture(Example):
    gl_version = (3, 3)
    aspect_ratio = 16 / 9
    title = "Simple Texture"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # Point coordinates are put followed by the vec3 color values
        vertices = np.array([
          0.5, 0.5, 0.0,     1.0, 1.0, # top right
          0.5, -0.5, 0.0,    1.0, 0.0, # bottom right
          -0.5, -0.5, 0.0,   0.0, 0.0, # bottom left
          -0.5, 0.5, 0.0,    0.0, 1.0  # top left
        ], dtype='f4')

        indices = np.array([
          0, 1, 3,
          1, 2, 3
        ], dtype='i4')

        self.vbo = self.ctx.buffer(vertices)
        self.ebo = self.ctx.buffer(indices)

        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vbo, '3f 2f', 'aPos', 'aTexCoord')
            ],
            self.ebo
        )
        self.texture = self.load_texture_2d('crate.png')

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.texture.use()
        self.vao.render()


if __name__ == '__main__':
    SimpleTexture.run()