import carla
import random
import time

'''
torque_curve=[
    Vector2D(x=0.000000, y=400.000000), 
    Vector2D(x=1890.760742, y=500.000000),
    Vector2D(x=5729.577637, y=400.000000)
], 
max_rpm=6300.000000, 
moi=1.000000,
damping_rate_full_throttle=0.150000, 
damping_rate_zero_throttle_clutch_engaged=2.000000,
damping_rate_zero_throttle_clutch_disengaged=0.350000, 
use_gear_autobox=True,
gear_switch_time=0.500000, 
clutch_strength=10.000000, 
final_ratio=4.000000,
forward_gears=[
    GearPhysicsControl(ratio=3.730000, down_ratio=0.200000, up_ratio=0.350000),
    GearPhysicsControl(ratio=2.050000, down_ratio=0.200000, up_ratio=0.350000),
    GearPhysicsControl(ratio=1.390000, down_ratio=0.200000, up_ratio=0.350000),
    GearPhysicsControl(ratio=1.030000, down_ratio=0.200000, up_ratio=0.350000),
    GearPhysicsControl(ratio=0.820000, down_ratio=0.200000, up_ratio=0.350000)
], 
mass=977.000000,
drag_coefficient=0.300000, 
center_of_mass=Location(x=0.750000, y=0.000000, z=-0.450000),
steering_curve=[
    Vector2D(x=0.000000, y=1.000000), 
    Vector2D(x=20.000000, y=0.897898),
    Vector2D(x=60.000000, y=0.760000), 
    Vector2D(x=120.000000, y=0.700000)
],
wheels=[
    WheelPhysicsControl(
        tire_friction=3.500000, 
        damping_rate=0.250000,
        max_steer_angle=45.000000, 
        radius=34.250000,
        max_brake_torque=1500.000000, 
        max_handbrake_torque=0.000000,
        position=Vector3D(x=4117.341797, y=-396.728882, z=35.893047)),
    WheelPhysicsControl(
        tire_friction=3.500000, 
        damping_rate=0.250000,
        max_steer_angle=45.000000, 
        radius=34.250000,
        max_brake_torque=1500.000000, 
        max_handbrake_torque=0.000000,
        position=Vector3D(x=4117.341797, y=-255.679199, z=35.893047)),
    WheelPhysicsControl(
        tire_friction=3.500000, 
        damping_rate=0.250000,
        max_steer_angle=0.000000, 
        radius=35.000000,
        max_brake_torque=1500.000000,
        max_handbrake_torque=3000.000000,
        position=Vector3D(x=3868.321533, y=-396.729004, z=35.893047)),
    WheelPhysicsControl(
        tire_friction=3.500000, 
        damping_rate=0.250000,
        max_steer_angle=0.000000, 
        radius=35.000000,
        max_brake_torque=1500.000000,
        max_handbrake_torque=3000.000000,
        position=Vector3D(x=3868.321533, y=-255.679108,z=35.888573))
]
'''

def to_string_list(list):
    return "\n".join(["\t"+str(obj) for obj in list])

def to_string_physics_control(pc):
    return f"""
max_rpm={pc.max_rpm}, 
moi={pc.moi},
damping_rate_full_throttle={pc.damping_rate_full_throttle}, 
damping_rate_zero_throttle_clutch_engaged={pc.damping_rate_zero_throttle_clutch_engaged},
damping_rate_zero_throttle_clutch_disengaged={pc.damping_rate_zero_throttle_clutch_disengaged},
use_gear_autobox={pc.use_gear_autobox},
gear_switch_time={pc.gear_switch_time}, 
clutch_strength={pc.clutch_strength}, 
final_ratio={pc.final_ratio},
mass={pc.mass},
drag_coefficient={pc.drag_coefficient}, 
center_of_mass={pc.center_of_mass},
torque_curve=[
{to_string_list(pc.torque_curve)}
],
forward_gears=[
{to_string_list(pc.forward_gears)}
],
steering_curve=[
{to_string_list(pc.steering_curve)}
],
wheels=[
{to_string_list(pc.wheels)}
]
"""


def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        world = client.get_world()
        map = world.get_map()

        spawn_points = map.get_spawn_points()

        blueprint_library = world.get_blueprint_library()
        for bp in blueprint_library.filter('vehicle'):
            print("=============================================")
            print(bp.id)

            vehicle = world.spawn_actor(bp, random.choice(spawn_points))
            pc = vehicle.get_physics_control()
            print(to_string_physics_control(pc))
            vehicle.destroy()
            time.sleep(0.5)
        time.sleep(2)

    finally:
        print('done.')

if __name__ == '__main__':
    main()
