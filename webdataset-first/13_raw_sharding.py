import webdataset as wds
import braceexpand
import torch


def my_split_by_node(urls):
    # node_id, node_count = torch.distributed.get_rank(), torch.distributed.get_world_size()
    # return urls[node_id::node_count]
    return urls


urls = list(braceexpand.braceexpand("dataset-{000000..000009}.tar"))
dataset = wds.ShardList(urls, splitter=wds.split_by_worker, nodesplitter=my_split_by_node, shuffle=False)

for item in dataset:
    print(item)

# dataset = wds.Processor(dataset, wds.url_opener)
# dataset = wds.Processor(dataset, wds.tar_file_expander)
# dataset = wds.Processor(dataset, wds.group_by_keys)