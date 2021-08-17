from typing import Dict
import torch
from torchvision import transforms
import webdataset as wds
from itertools import islice


def identity(x):
    return x

normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225])

preproc = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    normalize,
])


url = "http://storage.googleapis.com/nvdata-openimages/openimages-train-{000000..000004}.tar"
url = f"pipe:curl -L -s {url} || true"
bs = 20

dataset = (
    wds.Dataset(url, length=int(1e9) // bs)
    .shuffle(100)
    .decode("pil")
    .to_tuple("jpg;png", "json")
    .map_tuple(preproc, identity)
    .batched(20)
)

dataloader = torch.utils.data.DataLoader(dataset, num_workers=4, batch_size=None)
images, targets = next(iter(dataloader))
print(images.shape, targets)
# torch.Size([20, 3, 224, 224])

'''
[
    [
        {'ImageID': 'f9cd8566b480753e', 'Source': 'activemil', 'LabelName': '/m/04yx4', 'Confidence': '1', 'XMin': '0.263915', 'XMax': '1.000000', 'YMin': '0.000000', 'YMax': '0.999167', 'IsOccluded': '1', 'IsTruncated': '1', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'},
        {'ImageID': 'f9cd8566b480753e', 'Source': 'xclick', 'LabelName': '/m/0dzct', 'Confidence': '1', 'XMin': '0.412133', 'XMax': '0.916198', 'YMin': '0.000000', 'YMax': '0.899167', 'IsOccluded': '0', 'IsTruncated': '1', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'}
    ],
    [
        {'ImageID': 'f807b724d26e5b03', 'Source': 'activemil', 'LabelName': '/m/03q69', 'Confidence': '1', 'XMin': '0.411875', 'XMax': '0.513125', 'YMin': '0.346667', 'YMax': '0.474167', 'IsOccluded': '1', 'IsTruncated': '0', 'IsGroupOf': '0', 'IsDepiction': '0', 'IsInside': '0'}
    ]
]     
'''