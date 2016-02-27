# Programmer: Anton Strickland
# Self-drawing program

from PIL import Image
import random

img = Image.open("bride.jpg")

new = Image.new("RGB", (100,100), (128, 128, 128))

for x in range(new.size[0]):
  for y in range(new.size[1]):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    new.putpixel((x,y),(r,g,b))

new.show()