import torch 
from functorch import grad

x = torch.randn([])
cos_x = grad(lambda x : torch.sin(x))(x)
assert torch.allclose(cos_x, x.cos())

# second-order
neg_sin_x = grad(grad(lambda x: torch.sin(x)))(x)
assert torch.allclose(neg_sin_x, -x.sin())

