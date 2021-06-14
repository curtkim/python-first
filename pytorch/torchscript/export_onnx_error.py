import torch


class RI(torch.nn.Module):
    def forward(self, X, repeat):
        return X.repeat_interleave(repeat, dim=0)


inputs = (torch.arange(5), torch.tensor(3))
torch.onnx.export(RI(), inputs, 'please_work.onnx', opset_version=11)
