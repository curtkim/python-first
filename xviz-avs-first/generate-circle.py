import os
import shutil
import xviz_avs.io as xi
from circle import CircleScenario

scenario = CircleScenario(live=False)

OUTPUT = "web/output"

if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)

#writer = xi.XVIZProtobufWriter(xi.DirectorySource(OUTPUT))
#writer = xi.XVIZGLBWriter(xi.DirectorySource(OUTPUT))
writer = xi.XVIZJsonWriter(xi.DirectorySource(OUTPUT))

writer.write_message(scenario.get_metadata_inner())
for t in range(0, 10):
    writer.write_message(scenario.get_message_inner(t/10))

writer.close()

shutil.copy("data/0-frame.json", "web/output/0-frame.json")