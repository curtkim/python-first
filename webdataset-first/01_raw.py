from typing import Dict
import torch
from torchvision import transforms
import webdataset as wds
from itertools import islice


dataset = wds.Dataset('openimages-train-000000.tar')

# islice(iterable, start, stop[, step])
sample: Dict

for sample in islice(dataset, 0, 2):
    # __key__, jpg, json 3개의 key를 가진다.
    for key, value in sample.items():
        # key : str
        # value : bytes
        print(key, repr(value)[:50])
    print()


'''
__key__ 'e39871fd9fd74f55'
jpg b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x01
json b'[{"ImageID": "e39871fd9fd74f55", "Source": "xcli

__key__ 'f18b91585c4d3f3e'
jpg b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00
json b'[{"ImageID": "f18b91585c4d3f3e", "Source": "acti
'''