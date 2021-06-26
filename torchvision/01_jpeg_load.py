import torchvision
from torchvision.io.image import read_file, decode_jpeg


print(torchvision.__version__)

data = read_file('car.jpg')  # raw data is on CPU
img = decode_jpeg(data, device='cuda')  # decoded image in on GPU
print(type(img), img.shape, img.dtype)
# <class 'torch.Tensor'> torch.Size([3, 2139, 3500]) torch.uint8

