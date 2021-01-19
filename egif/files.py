import numpy as np 
from PIL import Image

from .image import EgifImage
from .encoder import encode, decode, to_16_bits, from_16_bits
from .utils import replace

__all__ = ['read', 'write', 'from_images', 'to_images', 'load', 'dump']


MARKER = 0x0FFF


def _get_sectors(data):
    sectors = []
    last = 0
    for i,d in enumerate(data):
        if d == MARKER:
            sectors.append(data[last : i])
            last = i + 1 # do not include the marker
    return sectors


def read(path):
    with open(path, 'rb') as file:
        bits = file.read()
    return load(bits)

def write(img, path='out.egif', quality=5):
    bits = dump(img, quality)
    with open(path, 'wb') as file:
        file.write(bits)
    return bits


def from_images(paths):
    images = []

    for path in paths:
        img = Image.open(path)
        frame = np.asarray(img)
        images.append(frame)
    
    matrix = np.stack(images)
    return EgifImage(matrix)

def to_images(img, path):
    pass


def load(bits):
    data = from_16_bits(bits)
    sectors = _get_sectors(data)
    
    header = sectors[0]
    r_dct = sectors[1]
    g_dct = sectors[2]
    b_dct = sectors[3]

    version, width, height, frames, quality, *args = header

    shape = (frames, height, width)
    
    r = decode(r_dct, shape, quality)
    g = decode(g_dct, shape, quality)
    b = decode(b_dct, shape, quality)

    matrix = np.stack((r,g,b), axis=3)
    return EgifImage(matrix)


def dump(img, quality=5):
    version = 0
    width = img.width
    height = img.height 
    frames = img.frames 

    r = encode(img.r, quality)
    g = encode(img.g, quality)
    b = encode(img.b, quality)

    header = [version, width, height, frames, quality]
    sectors = [header, r, g, b]

    # assert that the MARKER is unique
    for sector in sectors:
        replace(sector, MARKER, MARKER+1)

    data = []
    for sector in sectors:
        data.extend(sector)
        data.append(MARKER)
    
    return to_16_bits(data)

