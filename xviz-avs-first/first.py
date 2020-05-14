import xviz_avs.io as xi
from circle import CircleScenario

scenario = CircleScenario()

#print(scenario.get_metadata())
#print(scenario.get_message(0))

source = xi.DirectorySource("output")
writer = xi.XVIZJsonWriter(source)
writer.write_message(scenario.get_metadata_inner())
writer.write_message(scenario.get_message_inner(0))
writer.write_message(scenario.get_message_inner(1))
writer.close()
