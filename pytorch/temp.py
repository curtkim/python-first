#from PIL import Image
import PIL
import cv2
import numpy

image_path = "input/car.jpg"

# This is a lazy operation; this function identifies the file, but
# the file remains open and the actual image data is not read from the file
# until you try to process the data (or call the load() method)
img = PIL.Image.open(image_path)
print(type(img))

img2 = cv2.imread(image_path)
assert isinstance(img2, numpy.ndarray)
