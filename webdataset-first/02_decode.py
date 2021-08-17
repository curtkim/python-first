from typing import Dict
import torch
from torchvision import transforms
import webdataset as wds
from itertools import islice


dataset = (
    wds.Dataset('openimages-train-000000.tar')
    .shuffle(100)
    .decode('pil')
    .to_tuple("jpg;png", "json")
)

for image, data in islice(dataset, 0, 2):
    # image: bytes
    # data: list of Dict
    print(repr(image)[:50], data)
    #print(image.shape, image.dtype, type(data))

'''
PIL.Image.Image image mode=RGB size=1024x684
[
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'activemil', 'LabelName': '/m/01bl7v', 'Confidence': '1', 'XMin': '0.726875', 'XMax': '0.836875', 'YMin': '0.540833', 'YMax': '0.889167', 'IsOccluded': '1','IsTruncated': '0', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'},
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'activemil', 'LabelName': '/m/04yx4', 'Confidence': '1', 'XMin': '0.771875', 'XMax': '0.935625', 'YMin': '0.255833', 'YMax': '0.905000', 'IsOccluded': '1', 'IsTruncated': '0', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'},
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'activemil', 'LabelName': '/m/07j7r', 'Confidence': '1', 'XMin': '0.013750', 'XMax': '0.240000', 'YMin': '0.046667', 'YMax': '0.660000', 'IsOccluded': '1', 'IsTruncated': '1', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'},
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'xclick', 'LabelName': '/m/07j7r', 'Confidence': '1', 'XMin': '0.233125', 'XMax': '0.999375', 'YMin': '0.000000', 'YMax': '0.350833', 'IsOccluded': '1', 'IsTruncated': '1', 'IsGroupOf': '1', 'IsDepiction': '0', 'IsInside': '0'},
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'xclick', 'LabelName': '/m/09j5n', 'Confidence': '1', 'XMin': '0.726875', 'XMax': '0.748750', 'YMin': '0.826667', 'YMax': '0.867500', 'IsOccluded': '0', 'IsTruncated': '0', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'},
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'xclick', 'LabelName': '/m/09j5n', 'Confidence': '1', 'XMin': '0.754375', 'XMax': '0.775000', 'YMin': '0.835000', 'YMax': '0.862500', 'IsOccluded': '0', 'IsTruncated': '0', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'},
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'xclick', 'LabelName': '/m/09j5n', 'Confidence': '1', 'XMin': '0.777500', 'XMax': '0.818750', 'YMin': '0.793333', 'YMax': '0.846667', 'IsOccluded': '0', 'IsTruncated': '0', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'},
    {'ImageID': 'e55592f306ec1b0b', 'Source': 'xclick', 'LabelName': '/m/09j5n', 'Confidence': '1', 'XMin': '0.826250', 'XMax': '0.862500', 'YMin': '0.797500', 'YMax': '0.846667', 'IsOccluded': '1', 'IsTruncated': '0', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'}
]
'''