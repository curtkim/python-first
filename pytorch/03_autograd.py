import torch

def test1():
    x = torch.ones(2, 2, requires_grad=True)
    print('x', x)

    y = x + 2
    print('y', y)

    z = y * y * 3
    out = z.mean()
    print('z', z, 'out', out)

    out.backward() #  is equivalent to out.backward(torch.tensor(1.))
    print(x.grad)


def test2():
    x = torch.arange(4, requires_grad=True, dtype=float)
    y = 2 * torch.dot(x, x)
    # y' = 4x

    assert torch.equal(y, torch.tensor(2*(1+4+9), dtype=float))

    y.backward()
    assert torch.equal(x.grad, torch.tensor([0, 4, 8, 12], dtype=float))


test2()
