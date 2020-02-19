from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32

import metric_pb2


with open('out.bin', 'wb') as f:
    my_tags = ("my_tag", "foo:bar")
    for i in range(128):
        my_metric = metric_pb2.Metric()
        my_metric.name = 'sys.cpu'
        my_metric.type = 'gauge'
        my_metric.value = i * 1.0
        size = my_metric.ByteSize()
        f.write(_VarintBytes(size))
        f.write(my_metric.SerializeToString())
