import cv2
import math
import numpy as np

from geometry_utils import *

import moderngl
import moderngl_window as mglw
from pyrr import Matrix44


def make_pointcloud_inner(rgb, depth):
    rgb_coords = np.transpose(rgb, (2,0,1)).reshape((3, -1))        # reshape (3, height*width)
    print(rgb_coords.shape)

    # Get intrinsic parameters
    height, width, _ = rgb.shape
    K = intrinsic_from_fov(height, width, 90)  # +- 45 degrees
    K_inv = np.linalg.inv(K)

    # Get pixel coordinates
    pixel_coords = pixel_coord_np(width, height)  # [3, npoints]

    # Apply back-projection: K_inv @ pixels * depth
    cam_coords = K_inv[:3, :3] @ pixel_coords * depth.flatten()

    # Limit points to 150m in the z-direction for visualisation
    cam_coords[[0,1,2]] = cam_coords[[2,0,1]]  # x,y,z축을 바꾼다.
    cam_coords[2,:] = cam_coords[2,:]*-1 # z축을 뒤집는
    cam_coords[0,:] = cam_coords[0,:]*-1 # x축을 뒤집는

    #aabb = pyrr.aabb.create_from_points(cam_coords)
    #print(cam_coords.shape, aabb)

    all_coords = np.vstack((cam_coords, rgb_coords))
    all_coords = all_coords[:, np.where(all_coords[0] > -150)[0]]

    all_coords = all_coords.T.astype('f4').copy()
    print('all_coords.shape', all_coords.shape)

    return all_coords


def make_pointcloud(rgb_file, depth_file):

    # Load images
    rgb = cv2.cvtColor(cv2.imread(rgb_file), cv2.COLOR_BGR2RGB)
    rgb = rgb.astype('f4')/255                                      # int -> float

    # Depth is stored as float32 in meters
    depth = cv2.imread(depth_file, cv2.IMREAD_ANYDEPTH)
    print('depth.shape', depth.shape)    

    return make_pointcloud_inner(rgb, depth)


def make_pointcloud2(rgb_file, depth_file):

    # Load images
    rgb = cv2.cvtColor(cv2.imread(rgb_file), cv2.COLOR_BGR2RGB)
    rgb = rgb.astype('f4')/255                                      # int -> float
    print('rgb.shape', rgb.shape)    

    # Depth is stored as float32 in meters
    depth_file = np.load(depth_file)
    depth = depth_file['depth']
    print('depth.shape', depth.shape)    

    return make_pointcloud_inner(rgb, depth[:rgb.shape[0],:rgb.shape[1]]) #TODO

#pc = make_pointcloud('rgb.png', 'depth.exr')
pc = make_pointcloud2('0000000000.png', '0000000000.npz')


vertex_shader = '''
    #version 330
    uniform mat4 mvp;
    
    in vec3 in_vert;
    in vec3 in_color;
    
    //out vec3 v_vert;
    out vec3 v_color;
    
    void main() {
        gl_Position = mvp * vec4(in_vert, 1.0);        
        v_color = in_color;//mix(vec3(0.0, 0.0, 1.0), vec3(0.0, 1.0, 0.0), abs(sin(in_vert.z)));
    }
'''
fragment_shader = '''
    #version 330
    in vec3 v_color;
    out vec4 f_color;
    
    void main() {
        f_color = vec4(v_color, 1.0);
    }
'''


class MyExample(mglw.WindowConfig):

    gl_version = (3, 3)
    title = "ModernGL Example"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    samples = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.mvp = self.prog['mvp']

        self.angleX = 0
        self.angleY = 0
        self.distance = 25
        self.origin = np.array([0.0,0.0,0.0])
        self.mouse_button = 0


        self.vbo = self.ctx.buffer(pc)

        # We control the 'in_vert' and `in_color' variables
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vbo, '3f 3f', 'in_vert', 'in_color')
            ],
        )

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 300.0)

        camera_pos = np.array([np.cos(self.angleY)*np.cos(self.angleX), np.sin(self.angleX), np.sin(self.angleY)]) * self.distance

        lookat = Matrix44.look_at(
            tuple(camera_pos+self.origin),  # eye
            tuple(self.origin),             # target
            (0.0, 0.0, 1.0),                # up
        )

        self.mvp.write((proj * lookat).astype('f4'))
        self.ctx.point_size = 10
        self.vao.render(moderngl.POINTS)


    def mouse_drag_event(self, x, y, dx, dy):
        if self.mouse_button == 2:
            self.angleX += dx * -0.01
            self.angleY += dy * 0.01
            self.angleY = min(max(self.angleY, 0), (math.pi-0.2) / 2)
        elif self.mouse_button == 1:
            self.origin += np.array([dy*-0.01, dx*-0.01, 0.0])

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.distance += y_offset * -0.1

    def mouse_press_event(self, x, y, button):
        self.mouse_button = button

    def mouse_release_event(self, x: int, y: int, button: int):
        self.mouse_button = 0

if __name__ == '__main__':
    mglw.run_window_config(MyExample)