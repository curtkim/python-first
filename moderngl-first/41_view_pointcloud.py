'''
    Added a simple camera class to an existing example.
    The camera class is built using following tutorials:
       https://learnopengl.com/Getting-started/Camera
       http://in2gpu.com/2016/03/14/opengl-fps-camera-quaternion/

    Controls:
        Move:
            Forward - W
            Backwards - S

        Strafe:
            Up - up arrow
            Down - down arrow
            Left - A
            Right - D

        Rotate:
            Left - Q
            Right - E

        Zoom:
            In - X
            Out - Z
'''

import os
import numpy as np

import moderngl
import moderngl_window as mglw

import open3d as o3d

from camera import Camera

vertex_shader = '''
    #version 330

    uniform mat4 Mvp;

    in vec3 in_vert;
    out vec4 frag_color;

    void main() {
        frag_color = mix(vec4(0.0, 0.0, 1.0, 1.0), vec4(0.0, 1.0, 0.0, 1.0), abs(sin(in_vert.z)));
        gl_Position = Mvp * vec4(in_vert, 1.0);
    }
'''
fragment_shader = '''
    #version 330

    in vec4 frag_color;
    out vec4 f_color;

    void main() {
        f_color = frag_color;
        //f_color = vec4(0.1, 0.1, 0.1, 1.0);
    }
'''


class PerspectiveProjection(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    samples = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.camera = Camera(self.aspect_ratio)
        self.mvp = self.prog['Mvp']

        pcd_load = o3d.io.read_point_cloud("./pc_000247.ply")
        xyz_load = np.asarray(pcd_load.points)

        self.vbo = self.ctx.buffer(xyz_load.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')

        self.states = {
            self.wnd.keys.W: False,     # forward
            self.wnd.keys.S: False,     # backwards
            self.wnd.keys.UP: False,    # strafe Up
            self.wnd.keys.DOWN: False,  # strafe Down
            self.wnd.keys.A: False,     # strafe left
            self.wnd.keys.D: False,     # strafe right
            self.wnd.keys.Q: False,     # rotate left
            self.wnd.keys.E: False,     # rotare right
            self.wnd.keys.Z: False,     # zoom in
            self.wnd.keys.X: False,     # zoom out
        }

    def move_camera(self):
        if self.states.get(self.wnd.keys.W):
            self.camera.move_forward()

        if self.states.get(self.wnd.keys.S):
            self.camera.move_backwards()

        if self.states.get(self.wnd.keys.UP):
            self.camera.strafe_up()

        if self.states.get(self.wnd.keys.DOWN):
            self.camera.strafe_down()

        if self.states.get(self.wnd.keys.A):
            self.camera.strafe_left()

        if self.states.get(self.wnd.keys.D):
            self.camera.strafe_right()

        if self.states.get(self.wnd.keys.Q):
            self.camera.rotate_left()

        if self.states.get(self.wnd.keys.E):
            self.camera.rotate_right()

        if self.states.get(self.wnd.keys.Z):
            self.camera.zoom_in()

        if self.states.get(self.wnd.keys.X):
            self.camera.zoom_out()

    def key_event(self, key, action, modifiers):
        if key not in self.states:
            print(key, action)
            return

        if action == self.wnd.keys.ACTION_PRESS:
            self.states[key] = True
        else:
            self.states[key] = False

    def render(self, time, frame_time):
        self.move_camera()

        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.mvp.write((self.camera.mat_projection * self.camera.mat_lookat).astype('f4'))
        self.vao.render(moderngl.POINTS)

        #print(time, frame_time)


if __name__ == '__main__':
    mglw.run_window_config(PerspectiveProjection)
