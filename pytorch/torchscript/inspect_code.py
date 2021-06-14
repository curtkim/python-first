import torch


@torch.jit.script
def foo(len: int) -> torch.Tensor:
    rv = torch.zeros(3, 4)
    for i in range(len):
        if i < 10:
            rv = rv - 1.0
        else:
            rv = rv + 1.0
    return rv


print(foo.code)
