from typing import Dict
import torch
from torchvision import transforms
import webdataset as wds
from itertools import islice

def add_noise(source, noise=0.01):
    for inputs, targets in source:
        inputs = inputs + noise * torch.randn_like(inputs)
        yield inputs, targets


#url = "http://storage.googleapis.com/nvdata-openimages/openimages-train-000000.tar"
#url = f"pipe:curl -L -s {url} || true"

url = "openimages-train-000000.tar"

dataset = wds.ShardList(url)
dataset = wds.Processor(dataset, wds.url_opener)
dataset = wds.Processor(dataset, wds.tar_file_expander)
dataset = wds.Processor(dataset, wds.group_by_keys)
dataset = wds.Processor(dataset, wds.shuffle, 100)
dataset = wds.Processor(dataset, wds.decode, wds.imagehandler("torchrgb"))
dataset = wds.Processor(dataset, wds.to_tuple, "png;jpg;jpeg", "json")
noisy_dataset = wds.Processor(dataset, add_noise, noise=0.02)

# short version
#dataset = wds.WebDataset(url).shuffle(100).decode("torchrgb").to_tuple("png;jpg;jpeg", "json")
#noisy_dataset = wds.Processor(dataset, add_noise, noise=0.02)


images, targets = next(iter(noisy_dataset))
print(images.shape)     # torch.Size([3, 683, 1024])

for target in targets:
    print(target)

