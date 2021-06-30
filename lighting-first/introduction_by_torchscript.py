import torch
loaded = torch.jit.load('mnist.ts')

print(loaded)
print(loaded.code)

x = torch.Tensor(1, 1, 28, 28)
out = loaded(x)
print(out)
