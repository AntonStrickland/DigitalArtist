# Programmer: Anton Strickland
# Self-drawing program

from PIL import Image
from sys import argv
import random

# Set the name of the image
name = ''
if len(argv) < 2:
  print("Please specify a file name for the image.")
  exit()
else:
  name = argv[1]
  
# Set the type of the image
fileType = ''
if len(argv) < 3:
  print("Please specify a file type for the image (JPEG, PNG, BMP).")
  exit()
else:
  fileType = argv[2]
  
new = Image.new("RGBA", (100,100), (128, 128, 128, 128))

for x in range(new.size[0]):
  for y in range(new.size[1]):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    new.putpixel((x,y),(r,g,b))

new.save("output/" + name + "." + fileType.lower(), fileType)