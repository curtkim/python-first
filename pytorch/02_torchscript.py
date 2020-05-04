import torchvision
import torch

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

img = torch.rand(1, 3, 2139, 3500)
print(img.shape)

scripted_model = torch.jit.script(model)
print(scripted_model.code)
scripted_model.save('fasterrcnn_resnet50_fpn.pt')