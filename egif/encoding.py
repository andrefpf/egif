import numpy as np
from struct import pack, unpack_from

from .image import EgifImage
from .transforms import DCT2D, DCT3D
from .utils import chunks_2d, chunks_3d
from .quantization import quantize, disquantize, get_2d_qtable, get_3d_qtable


MARKER = 0x0FFF

# BITS CONVERSION
def to_16_bits(data):
    fmt = 'h' * len(data)
    return pack('>' + fmt, *data)

def from_16_bits(data):
    fmt = 'h' * (len(data) // 2) # 16 bits = 2 bytes
    return unpack_from('>' + fmt, data)


# TRANSFORMATION IN CHUNKS
def transform_2d(matrix):
    dct = DCT2D(8, 8)
    table = get_2d_qtable((8,8))
    compressed = matrix.copy()

    for chunk in chunks_2d(compressed):
        dct.foward(chunk)
        quantize(chunk, table)
    return compressed

def distransform_2d(matrix):
    dct = DCT2D(8, 8)
    table = get_2d_qtable((8,8))
    compressed = matrix.copy()

    for chunk in chunks_2d(compressed):
        disquantize(chunk, table)
        dct.inverse(chunk)
    return compressed

def transform_3d(matrix):
    dct = DCT3D(8, 8, 8)
    table = get_3d_qtable((8,8,8), 30)
    compressed = matrix.copy()

    for chunk in chunks_3d(compressed):
        dct.foward(chunk)
        quantize(chunk, table)
    return compressed

def distransform_3d(matrix):
    dct = DCT3D(8, 8, 8)
    table = get_3d_qtable((8,8,8), 30)
    compressed = matrix.copy()

    for chunk in chunks_3d(compressed):
        disquantize(chunk, table)
        dct.inverse(chunk)
    return compressed


# DATA PACKAGING
def dump(image):
    version = 0
    width = image.width
    height = image.height 
    frames = image.frames

    if frames == 1:
        y = transform_2d(image.y).flatten()
        cb = transform_2d(image.cb).flatten()
        cr = transform_2d(image.cr).flatten()
    elif frames > 1:
        y = transform_3d(image.y).flatten()
        cb = transform_3d(image.cb).flatten()
        cr = transform_3d(image.cr).flatten()
    else:
        raise ValueError('Frames should be equal or greater than 1')

    header = [version, width, height, frames]
    sectors = [header, y, cb, cr]

    # ensure that the mark is unique
    for i in range(len(sectors)):
        for j in range(len(sectors[i])):
            if MARKER == sectors[i][j]:
                sectors[i][j] += 1 

    data = []
    for sector in sectors:
        data.extend(sector)
        data.append(MARKER)

    compressed = run_length_encode(data)
    return to_16_bits(compressed)

def load(bits):
    data = from_16_bits(bits)
    decompressed = run_length_decode(data)
    
    sectors = []
    last = 0
    for i,d in enumerate(decompressed):
        if d == MARKER:
            sectors.append(decompressed[last : i])
            last = i + 1 # do not include markers

    header = sectors[0]
    version, width, height, frames, *args = header

    y_dct = np.array(sectors[1])
    cb_dct = np.array(sectors[2])
    cr_dct = np.array(sectors[3])

    if frames == 1:
        y = distransform_2d(y_dct.reshape(height, width))
        cb = distransform_2d(cb_dct.reshape(height, width))
        cr = distransform_2d(cr_dct.reshape(height, width))
    elif frames > 1:
        y = distransform_3d(y_dct.reshape(frames, height, width))
        cb = distransform_3d(cb_dct.reshape(frames, height, width))
        cr = distransform_3d(cr_dct.reshape(frames, height, width))
    else:
        raise ValueError('Frames should be equal or greater than 1')

    image = EgifImage((y,cb,cr), mode='ycbcr')
    return image


# ACTUAL COMPRESSION
def run_length_encode(array):
    # code to remove repetitions of the number 0
    repeted = 0
    encoded = []

    for i in array:
        if i == 0:
            repeted += 1
        elif repeted:
            encoded.append(0)
            encoded.append(repeted)
            encoded.append(i)
            repeted = 0
        else:
            encoded.append(i)

    if repeted:
        encoded.append(0)
        encoded.append(repeted)
    return encoded

def run_length_decode(array):
    last_was_zero = False
    decoded = []

    for i in array:
        if i == 0:
            last_was_zero = True
        elif last_was_zero:
            decoded.extend([0] * i)
            last_was_zero = False
        else:
            decoded.append(i)
    return decoded

