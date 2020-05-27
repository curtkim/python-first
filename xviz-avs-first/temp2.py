from PIL import Image
from numpy import asarray

image = Image.open('cat.jpg')
data = asarray(image)

print(data.shape)
