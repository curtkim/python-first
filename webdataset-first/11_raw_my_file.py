from typing import Dict
import torch
from torchvision import transforms
import webdataset as wds
from itertools import islice


dataset = wds.Dataset('voc.tar')

# islice(iterable, start, stop[, step])
sample: Dict

for sample in dataset:
    # __key__, jpg, json 3개의 key를 가진다.
    for key, value in sample.items():
        # key : str
        # value : bytes
        print(key, repr(value)[:50])
    print()


'''
__key__ './2007_000027'
jpg b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00
xml b'<annotation>\n\t<folder>VOC2012</folder>\n\t<fil

__key__ './2007_000032'
jpg b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00
xml b'<annotation>\n\t<folder>VOC2012</folder>\n\t<fil
'''