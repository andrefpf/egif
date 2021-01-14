import numpy as np
from scipy import fft
from time import time
from struct import pack, unpack_from

from .transforms import DCT2D, DCT3D
from .utils import chunks_2d, chunks_3d
from .quantization import quantize, disquantize, get_2d_qtable, get_3d_qtable


def to_16_bits(data):
    fmt = 'h' * len(data)
    return pack('>' + fmt, *data)

def from_16_bits(data):
    fmt = 'h' * (len(data) // 2) # 16 bits = 2 bytes
    return unpack_from('>' + fmt, data)

def encode(matrix):
    dct = DCT3D(8, 8, 8)
    table = get_3d_qtable((8,8,8))
    matrix = matrix.copy()

    a = matrix.copy()
    for chunk in chunks_3d(matrix):
        dct.foward(chunk)
        # chunk[:] = fft.dct(chunk)
        quantize(chunk, table)

    array = run_length_encode(matrix.flatten())
    return array

def decode(array, shape):
    dct = DCT3D(8, 8, 8)
    table = get_3d_qtable((8,8,8))
 
    matrix = run_length_decode(array)
    matrix = np.array(matrix)
    matrix = matrix.reshape(shape)

    for chunk in chunks_3d(matrix):
        disquantize(chunk, table)
        # chunk[:] = fft.idct(chunk)
        dct.inverse(chunk)
    return matrix

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
