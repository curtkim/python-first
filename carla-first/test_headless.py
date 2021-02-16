import carla


t = carla.Transform(carla.Location(0,0,0), carla.Rotation(0, 0 ,0))
print(t.get_forward_vector())
print(t.get_right_vector())

t = carla.Transform(carla.Location(0,0,0), carla.Rotation(0, 45 ,0))
print(t.get_forward_vector())
print(t.get_right_vector())

t = carla.Transform(carla.Location(0,0,0), carla.Rotation(0, 90 ,0))
print(t.get_forward_vector())
print(t.get_right_vector())

