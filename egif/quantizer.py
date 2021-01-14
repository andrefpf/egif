import numpy as np 
from functools import lru_cache

from .utils import sigmoid


# it is not actually used but that's a nice thing to make tests
# i also dont want to write all these values again if needed
JPEG_QUANTIZATION_TABLE = np.array([
    [16, 11, 10, 16, 24,  40,  51,  61],
    [12, 12, 14, 19, 26,  58,  60,  55],
    [14, 13, 16, 24, 40,  57,  69,  56],
    [14, 17, 22, 29, 51,  87,  80,  62],
    [18, 22, 37, 56, 68,  109, 103, 77],
    [24, 35, 55, 64, 81,  104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

def get_2d_qtable(shape, quality=5):
    if not (1 <= quality <= 5):
        raise ValueError('Quality parameter should be between 1 and 5')

    height, width = shape
    table = np.zeros(shape)  

    for h in range(height):
        for w in range(width):
            table[h,w] = 200 - sigmoid(h + w - height - width) * quality * 20
    return table.astype(int)

def get_3d_qtable(shape, quality=5):
    if not (1 <= quality <= 5):
        raise ValueError('Quality parameter should be between 1 and 5')

    frames, height, width = shape
    table = np.ones(shape, dtype=int)  

    a = (6 - quality) * 100  # rise up the maximum value
    b = 0.5                  # smooths the curve 

    for f in range(frames):
        for h in range(height):
            for w in range(width):
                exponent = -b * (f+1) * (h+1) * (w+1)
                table[f,h,w] = a * (1 - np.exp(exponent)) + 1

    return table 

def quantize(matrix, qtable):
    matrix[:] = np.round(matrix / qtable)
    return matrix

def disquantize(matrix, qtable):
    matrix[:] = matrix * qtable
    return matrix
