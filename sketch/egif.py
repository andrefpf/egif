from ctypes import *
import numpy as np

egif = CDLL('./egif.so')

def dwt(array, levels):
    pointer = array.ctypes.data_as(POINTER(c_int))
    egif.dwt(pointer, len(array), levels, 1)
    return array

def dwt_2d(matrix, levels):
    h, w = matrix.shape

    pointer = matrix.ctypes.data_as(POINTER(c_int))
    egif.dwt_2d(pointer, w, h, levels)
    return matrix

def dwt_3d(matrix, levels):
    f, h, w = matrix.shape

    pointer = matrix.ctypes.data_as(POINTER(c_int))
    egif.dwt_3d(pointer, w, h, f, levels)
    return matrix


def rgb_to_ycocg(matrix):
    c, h, w = matrix.shape

    pointer = matrix.ctypes.data_as(POINTER(c_int))
    egif.rgb_to_ycocg(pointer, h*w)
    return matrix
    

def ycocg_to_rgb(matrix):
    c, h, w = matrix.shape

    pointer = matrix.ctypes.data_as(POINTER(c_int))
    egif.ycocg_to_rgb(pointer, h*w)
    return matrix
