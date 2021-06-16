import torchvision
from torchvision.io.image import read_file, decode_jpeg


print(torchvision.__version__)

data = read_file('car.jpg')  # raw data is on CPU
img = decode_jpeg(data, device='cuda')  # decoded image in on GPU
print(img.shape, img.dtype)

