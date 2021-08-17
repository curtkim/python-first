from typing import Dict
import torch
from torchvision import transforms
import webdataset as wds
from itertools import islice

url = 'openimages-train-000000.tar'

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

dataset = (
    wds.Dataset(url)
    .shuffle(100)
    .decode("pil")
    .to_tuple("jpg;png", "json")
    .map_tuple(preproc, identity)
)

for image, data in islice(dataset, 0, 3):
    print(image.shape, image.dtype, type(data))

'''
torch.Size([3, 224, 224]) torch.float32 <class 'list'>
torch.Size([3, 224, 224]) torch.float32 <class 'list'>
torch.Size([3, 224, 224]) torch.float32 <class 'list'>
'''