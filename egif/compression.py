from .image import chunks_2d, chunks_3d
from .transforms import DCT, DCT2D, DCT3D
from .quantization import quantize, disquantize, get_quantization_table

def compress_2d(matrix):
    dct = DCT2D(8, 8)
    compressed = matrix.copy()
    for chunk in chunks_2d(compressed):
        dct.foward(chunk)
    return compressed

def decompress_2d(matrix):
    dct = DCT2D(8, 8)
    compressed = matrix.copy()
    for chunk in chunks_2d(compressed):
        dct.inverse(chunk)
    return compressed

def compress_3d(matrix):
    dct = DCT3D(8, 8, 8)
    compressed = matrix.copy()
    for chunk in chunks_3d(compressed):
        dct.foward(chunk)
    return compressed

def decompress_3d(matrix):
    dct = DCT3D(8, 8, 8)
    compressed = matrix.copy()
    for chunk in chunks_3d(compressed):
        dct.inverse(chunk)
    return compressed
