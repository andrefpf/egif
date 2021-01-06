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

@lru_cache()
def get_quantization_table(shape, quality):
    h,w = shape
    table = np.zeros(shape)  

    for i in range(h):
        for j in range(w):
            table[i,j] = 200 - sigmoid(i+j-h-w) * quality 

    return table.astype(int)

def quantize(matrix, quality=100):
    table = get_quantization_table(matrix.shape, quality)
    matrix[:] = np.round(matrix / table)

def disquantize(matrix, quality=100):
    table = get_quantization_table(matrix.shape, quality)
    matrix[:] = matrix * table
