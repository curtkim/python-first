import torch


def loop_in_traced_fn(x):
    result = x[0]
    for i in range(x.size(0)):
        result = result * x[i]
    return result


inputs = (torch.rand(3, 4, 5),)
check_inputs = [(torch.rand(4, 5, 6),), (torch.rand(2, 3, 4),)]


traced = torch.jit.trace(loop_in_traced_fn, inputs, check_inputs=check_inputs)