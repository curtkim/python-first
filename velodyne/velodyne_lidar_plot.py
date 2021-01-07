"""
 - sudo apt install python3.5
 - sudo apt install python3-pip
 - pip3 install h5py
 - pip3 install pandas
 - pip3 install vispy
 - import vispy; vispy.test()
 - Find all data files over here : https://drive.google.com/open?id=1F3zh_eJcXMYRZ-tqBuk6331TyvjdKYaA
"""

import os
import time
import h5py
import numpy as np
import pandas as pd

import vispy.scene
from vispy.scene import visuals

t = -1
data_type = 'csv'
#data_type = 'h5'


def load_data(file_data):
    print(file_data)
    df = pd.read_csv(os.path.join(PATH, file_data), usecols=["Points_m_XYZ:0", "Points_m_XYZ:1", "Points_m_XYZ:2", "intensity"])
    matrix = df[["Points_m_XYZ:0", "Points_m_XYZ:1", "Points_m_XYZ:2"]].values

    # print (df['Points_m_XYZ:2'].describe())
    colors = []
    zs = []
    for i, row in df.iterrows():
        x = row['intensity'] / 255.0
        z = row['Points_m_XYZ:2']
        if z < -2:  # this is just random atm
            colors.append((0, 1, 0, .5))
        else:
            colors.append((x, x, x, .5))

    return (matrix, colors)


def update(data):
    t0 = time.time()
    matrix, colors = data
    t1 = time.time()
    scatter.set_data(matrix,
                     edge_color=None,
                     face_color=colors,
                     size=4)


"""
- Get Data
"""
t0 = time.time()
if data_type == 'h5':
    url_hdf5 = 'vispy_data.h5'
    points = []
    colors = []
    with h5py.File(url_hdf5, "r") as hf:
        for name in hf:
            if 'points' in name:
                points.append(np.array(hf.get(name)))
            if 'colors' in name:
                colors.append(np.array(hf.get(name)))

elif data_type == 'csv':
    #PATH = './HDL32-V2_Monterey Highway'
    PATH = './tmp'
    files = sorted(os.listdir(PATH))
    points, colors = [], []
    for i, f in enumerate(sorted(files)):
        if i != 2:
            continue
        points_, colors_ = load_data(f)
        points.append(points_)
        colors.append(colors_)

print('\n - Total Time taken for data read : ', round(time.time() - t0, 2), 's')

"""
# Build Canvas
"""
canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.bgcolor = '#111111'
view.camera = ['perspective', 'panzoom', 'fly', 'arcball', 'base', 'turntable', None][2]
if 1:
    view.camera.fov = 60
    view.camera.scale_factor = 0.7
    view.camera.keymap['Right'] = (1, 5)
    view.camera.keymap['Left'] = (-1, 5)
    view.camera.keymap['Up'] = (1, 4)
    view.camera.keymap['Down'] = (-1, 4)

print(' - Camera View : ', view.camera)
axis = visuals.XYZAxis(parent=view.scene)
scatter = visuals.Markers(parent=view.scene)
canvas.show()

# Update
t = min(t + 1, len(points) - 1)
update([points[t], colors[t]])


@canvas.events.key_press.connect
def keypress(e):
    global t
    if e._key.name == '=':
        print('  - File Index : ', t)
        t = min(t + 1, len(points) - 1)
        update([points[t], colors[t]])

    elif e._key.name == '-':
        print('  - File Index : ', t)
        t = max(t - 1, 0)
        update([points[t], colors[t]])

    else:
        print(' - key : ', e._key.name)


# @canvas.events.mouse_wheel.connect
# def mousewheel(e):
#     print (e, e._type, '||', e._button)
#     print (dir(e))

if __name__ == '__main__':
    import sys

    if sys.flags.interactive != 1:
        vispy.app.run()