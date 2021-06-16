# from https://hulk89.github.io/pytorch/2019/09/30/pytorch_dataset/

import torch
import numpy as np
from torch.utils.data import Dataset, ConcatDataset, Sampler, RandomSampler, BatchSampler, DataLoader


class VarMapDataset(Dataset):
    def __len__(self):
        return 10

    def __getitem__(self, idx):
        return {"input": torch.tensor([idx] * (idx + 1), dtype=torch.float32),
                "label": torch.tensor(idx, dtype=torch.float32)}

var_map_dataset = VarMapDataset()

dataloader = torch.utils.data.DataLoader(var_map_dataset)
for data in dataloader:
    print(data['label'], data['input'])

# collate_fn
print("--- collate_fn")
def make_batch(samples):
    """
        [0]
        [1 1]
        [2 2 2]
        ->
        [0 0 0
         1 1 0
         2 2 2] 으로 변경
    """
    inputs = [sample['input'] for sample in samples]
    labels = [sample['label'] for sample in samples]
    padded_inputs = torch.nn.utils.rnn.pad_sequence(inputs, batch_first=True)
    # print('debug', inputs, padded_inputs)
    return {'input': padded_inputs.contiguous(),
            'label': torch.stack(labels).contiguous()}


dataloader = torch.utils.data.DataLoader(var_map_dataset,
                                         batch_size=3,
                                         collate_fn=make_batch)
for data in dataloader:
    print(data['label'], data['input'])
