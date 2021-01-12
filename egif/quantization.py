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

def get_2d_qtable(shape, quality=100):
    h,w = shape
    table = np.zeros(shape)  
    for i in range(h):
        for j in range(w):
            table[i,j] = 200 - sigmoid(i+j-h-w) * quality 
    return table.astype(int)

def get_3d_qtable(shape, quality=100):
    frames, height, width = shape
    table = np.zeros(shape)  

    for f in range(frames):
        for h in range(height):
            for w in range(width):
                table[f,h,w] = 1 + f + h + w

    return table * quality

def quantize(matrix, qtable):
    matrix[:] = np.round(matrix / qtable)

def disquantize(matrix, qtable):
    matrix[:] = matrix * qtable
