import numpy as np
import math
import carla
from pyrr import Matrix44, Vector3
from itertools import chain


def tf2matrix4(tf : carla.Transform) -> Matrix44:
    t = Matrix44.from_translation([tf.location.x, tf.location.y, tf.location.z])
    r = Matrix44.from_eulers([tf.rotation.roll * math.pi / 180, tf.rotation.pitch * math.pi / 180, tf.rotation.yaw * math.pi / 180])
    return r*t


def tf2matrix4list(tf : carla.Transform) -> list:
    '''
    tf를 matrix4로 변환하고, 16개 원소의 list로 반환
    '''
    return list(chain.from_iterable(tf2matrix4(tf)))


if __name__ == "__main__":
    mat4 = tf2matrix4(carla.Transform(
        carla.Location(1,1,1),
        carla.Rotation(0,0,0)
    ))
    assert [1, 1, 1] == mat4 * Vector3([0, 0, 0])

    mat4 = tf2matrix4(carla.Transform(
        carla.Location(0, 0, 0),
        carla.Rotation(0, 0, 90)
    ))
    assert np.allclose([0, 0, -1], mat4 * Vector3([0, 1, 0]))

    flatten_list = tf2matrix4list(carla.Transform(
        carla.Location(0, 0, 0),
        carla.Rotation(0, 0, 90)
    ))

    print(mat4)
    print(flatten_list)