import numpy as np
from PIL import Image
import moderngl

ctx = moderngl.create_context(standalone=True, backend='egl')
fbo = ctx.simple_framebuffer((512, 512), components=4)
fbo.use()

vertices = np.array([
    -1.0,  -1.0,   1.0, 0.0, 0.0,
     1.0,  -1.0,   0.0, 1.0, 0.0,
     0.0,   1.0,   0.0, 0.0, 1.0],
    dtype='f4',
)

prog = ctx.program(vertex_shader="""
#version 330
in vec2 in_vert;
in vec3 in_color;
out vec3 color;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    color = in_color;
}
""",
fragment_shader="""
#version 330
out vec4 fragColor;
in vec3 color;
void main() {
    fragColor = vec4(color, 1.0);
}
""",
)

vao = ctx.simple_vertex_array(prog, ctx.buffer(vertices), 'in_vert', 'in_color')
vao.render(mode=moderngl.TRIANGLES)

image = Image.frombytes('RGBA', (512, 512), fbo.read(components=4))
image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save('output/triangle.png', format='png')