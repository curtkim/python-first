from google.protobuf.internal.decoder import _DecodeVarint32

import metric_pb2


with open('out.bin', 'rb') as f:
    buf = f.read()
    n = 0
    while n < len(buf):
        msg_len, new_pos = _DecodeVarint32(buf, n)
        n = new_pos
        msg_buf = buf[n:n+msg_len]
        n += msg_len
        read_metric = metric_pb2.Metric()
        read_metric.ParseFromString(msg_buf)
        print(read_metric.value)
        # do something with read_metric