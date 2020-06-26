# from https://hulk89.github.io/pytorch/2019/09/30/pytorch_dataset/

import torch
import numpy as np
from torch.utils.data import Dataset, ConcatDataset, Sampler, RandomSampler, BatchSampler, DataLoader


class MapDataset(Dataset):
    def __len__(self):
        return 10

    def __getitem__(self, idx):
        return {"input": torch.tensor([idx, 2 * idx, 3 * idx],dtype=torch.float32),
                "label": torch.tensor(idx,dtype=torch.float32)}

map_dataset = MapDataset()

# basic
dataloader = torch.utils.data.DataLoader(map_dataset)
for data in dataloader:
    print(data['label'], data['input'])

# batch_size
print("--- batch_size")
dataloader = torch.utils.data.DataLoader(map_dataset,batch_size=4)
for data in dataloader:
    print(data['input'].shape, data['label'])

# sampler
print("--- sampler")
point_sampler = RandomSampler(map_dataset)
dataloader = torch.utils.data.DataLoader(map_dataset,batch_size=4,sampler=point_sampler)
for data in dataloader:
    print(data['input'].shape, data['label'])

# batch sampler
print("--- batch sampler")
point_sampler = RandomSampler(map_dataset)
batch_sampler = BatchSampler(point_sampler, 3, False)
dataloader = torch.utils.data.DataLoader(map_dataset, batch_sampler=batch_sampler)
for data in dataloader:
    print(data['input'].shape, data['label'])


print("--- variable length dataset")
class VarMapDataset(Dataset):
    def __len__(self):
        return 10

    def __getitem__(self, idx):
        return {"input": torch.tensor([idx] * (idx + 1),dtype=torch.float32),
                "label": torch.tensor(idx,dtype=torch.float32)}

var_map_dataset = VarMapDataset()
dataloader = torch.utils.data.DataLoader(var_map_dataset)
for data in dataloader:
    print(data['input'])

# collate_fn
print("--- collate_fn")

