from PIL import Image


path = 'examples/high/0.jpg'
size = (1080, 720)

img = Image.open(path).resize(size)
img.save('examples/high/teste.png')