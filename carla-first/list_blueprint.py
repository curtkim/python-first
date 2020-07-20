import carla

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

world = client.get_world()

blueprints = [bp for bp in world.get_blueprint_library().filter('static.*')]
for blueprint in blueprints:
   print(blueprint.id)
   for attr in blueprint:
       print('  - {}'.format(attr))