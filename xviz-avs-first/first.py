import xviz_avs.io as xi
from circle import CircleScenario

scenario = CircleScenario(live=False)

#, xi.XVIZGLBWriter(xi.DirectorySource("output_glb"))
writer = xi.XVIZJsonWriter(xi.DirectorySource("output"))
writer.write_message(scenario.get_metadata_inner())
writer.write_message(scenario.get_message_inner(0))
writer.write_message(scenario.get_message_inner(1))
writer.close()

