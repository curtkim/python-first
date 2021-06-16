#http://theorangeduck.com/page/visualizing-rotation-spaces
import numpy as np
from mayavi import mlab

""" General Functions """

def quat_from_angle_axis(angle, axis):
    c = np.cos(angle / 2.0)
    s = np.sin(angle / 2.0)
    return np.concatenate([c[...,None], s[...,None] * axis], axis=-1)

def quat_mul(x, y):
    
    x0, x1, x2, x3 = x[...,0:1], x[...,1:2], x[...,2:3], x[...,3:4]
    y0, y1, y2, y3 = y[...,0:1], y[...,1:2], y[...,2:3], y[...,3:4]

    return np.concatenate([
        y0 * x0 - y1 * x1 - y2 * x2 - y3 * x3,      
        y0 * x1 + y1 * x0 - y2 * x3 + y3 * x2,   
        y0 * x2 + y1 * x3 + y2 * x0 - y3 * x1,    
        y0 * x3 - y1 * x2 + y2 * x1 + y3 * x0], axis=-1)

def quat_from_euler(x):
    r0 = quat_from_angle_axis(x[...,0], np.array([1,0,0]))
    r1 = quat_from_angle_axis(x[...,1], np.array([0,1,0]))
    r2 = quat_from_angle_axis(x[...,2], np.array([0,0,1]))
    return quat_mul(r2, quat_mul(r1, r0))

def quat_log(q, eps=1e-8):
    length = np.sqrt(np.sum(q[...,1:]*q[...,1:], axis=-1))
    return np.where((length < eps)[...,None],
        q[...,1:],
        (np.arctan2(length, q[...,0]) / length)[...,None] * q[...,1:])

def lerp(x, y, a):
    return (1.0 - a) * x + a * y

def log_color(x, eps=1e-8):
    length = np.sqrt(np.sum(x*x, axis=-1))
    color = ((x / length[...,None]) + 1.0) / 2.0
    grey = np.array([0.5, 0.5, 0.5])
    return np.where((length < eps)[...,None],
        grey,
        lerp(grey, color, 1 - (np.cos(2 * length)[...,None] + 1) / 2))

def plot(position, color, opacity, scale=0.5):
    
    # Convert to uint8
    rgba = np.concatenate([color, opacity[...,None]], axis=-1)
    rgba = np.clip(255 * rgba, 0, 255).astype(np.uint8)

    # plot the points
    pts = mlab.pipeline.scalar_scatter(
        position[...,0].ravel(), 
        position[...,1].ravel(), 
        position[...,2].ravel())
    
    # assign the colors to each point
    pts.add_attribute(rgba.reshape([-1, 4]), 'colors') 
    pts.data.point_data.set_active_scalars('colors')
    
    # set scaling for all the points
    g = mlab.pipeline.glyph(pts, transparent=True)
    g.glyph.glyph.scale_factor = scale 
    g.glyph.scale_mode = 'data_scaling_off'

""" Euler Angles Visualization """

mlab.figure(size=(640, 600))

position = []
for x in np.linspace(-2*np.pi, 4*np.pi, 35):
    for y in np.linspace(-2*np.pi, 4*np.pi, 35):
        for z in np.linspace(-2*np.pi, 4*np.pi, 35):
            position.append(np.array([x, y, z]))
            
position = np.array(position)

color = log_color(quat_log(quat_from_euler(position)))

inner_distance = np.max(abs(position - np.clip(position, 0, 2*np.pi)), axis=-1)
inner_factor = inner_distance / (2*np.pi)
inner_mask = inner_distance < 1e-5

opacity = np.ones_like(position[...,0])
opacity[ inner_mask] = 0.25
opacity[~inner_mask] = lerp(0.06, 0.0, inner_factor[~inner_mask])

plot(position, color, opacity, 0.5)

ax = mlab.axes(
    extent=[0, 2*np.pi, 0, 2*np.pi, 0, 2*np.pi], 
    ranges=[0, 2*np.pi, 0, 2*np.pi, 0, 2*np.pi])
ax.axes.label_format = ''
ax.axes.font_factor = 0.75
mlab.outline(extent=[0, 2*np.pi, 0, 2*np.pi, 0, 2*np.pi])
mlab.show()

""" Quaternions Visualization """

mlab.figure(size=(640, 600))

def fibonacci_sphere(samples=1):

    points = []
    phi = np.pi * (3. - np.sqrt(5.)) 

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2
        radius = np.sqrt(1 - y * y)

        theta = phi * i

        x = np.cos(theta) * radius
        z = np.sin(theta) * radius

        points.append((x, y, z))

    return points

position = np.array(fibonacci_sphere(1500))

# Swap position for better looking distribution
position = np.concatenate([
    position[...,0:1],
    position[...,2:3],
    position[...,1:2],
    ], axis=-1)

# Color with w on vertical axis
color = log_color(quat_log(np.concatenate([
    position[...,2:3], 
    position[...,0:1], 
    position[...,1:2], 
    np.zeros_like(position[...,0:1])
], axis=-1)))

# Fixed opacity
opacity = 0.3 * np.ones_like(position[...,0])

plot(position, color, opacity, 0.1)

ax = mlab.axes(
    extent=[-1, 1, -1, 1, -1, 1], 
    ranges=[-1, 1, -1, 1, -1, 1],
    xlabel='X',
    ylabel='Y',
    zlabel='W')
ax.axes.label_format = '%3.0f'
ax.axes.font_factor = 0.75

mlab.outline(extent=[-1, 1, -1, 1, -1, 1])
mlab.show()

""" Exponential Map Visualization """

mlab.figure(size=(640, 600))

position = []
for x in np.linspace(-2*np.pi, 2*np.pi, 25):
    for y in np.linspace(-2*np.pi, 2*np.pi, 25):
        for z in np.linspace(-2*np.pi, 2*np.pi, 25):
            point = np.array([x, y, z])
            length = np.sqrt(np.sum(point*point, axis=-1))
            if length < 2*np.pi:
                position.append(point)

position = np.array(position)

color = log_color(position)

inner_length = np.sqrt(np.sum(position*position, axis=-1))
inner_mask = inner_length < np.pi
inner_factor = np.maximum(inner_length - np.pi, 0.0) / np.pi

opacity = np.ones_like(position[...,0])
opacity[ inner_mask] = 0.25
opacity[~inner_mask] = lerp(0.06, 0.0, inner_factor)[~inner_mask]

plot(position, color, opacity, 0.4)

ax = mlab.axes(
    extent=[-np.pi, np.pi, -np.pi, np.pi, -np.pi, np.pi], 
    ranges=[-np.pi, np.pi, -np.pi, np.pi, -np.pi, np.pi],
    nb_labels=0)
ax.axes.label_format = ''
ax.axes.font_factor = 0.75

mlab.outline(extent=[-np.pi, np.pi, -np.pi, np.pi, -np.pi, np.pi])
mlab.show()

