import torch
from functorch import vmap, grad

batch_size, feature_size = 3,5

def model(weights, feature_vec):
    assert feature_vec.dim() == 1
    return feature_vec.dot(weights).relu()

def compute_loss(weights, example, target):
    y = model(weights, example)
    return ((y-target) *2).mean()

weights = torch.randn(feature_size, requires_grad=True)
examples = torch.randn(batch_size, feature_size)
targets = torch.randn(batch_size)
inputs = (weights, examples, targets)
grad_weight_per_example = vmap(grad(compute_loss), in_dims=(None, 0, 0))(*inputs)

