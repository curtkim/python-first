import torch


class RW(torch.nn.Module):
    def forward(self, X, repeat):
        X = X.reshape(1, *X.size()).expand(repeat, *X.size())
        return torch.cat(torch.unbind(X, dim=1))


inputs = (torch.arange(5), torch.tensor(3))
torch.onnx.export(RW(), inputs, 'please_work.onnx', opset_version=11)
