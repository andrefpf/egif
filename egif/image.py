import numpy as np 
from .dct import dct, idct


def zigzag_matrix(matrix):
    height, width = matrix.shape
    array = np.zeros(height * width)
    for n, (i,j) in enumerate(zig_zag(height, width)):
        array[n] = matrix[i,j]
    return array

def zig_zag_array(array, shape):
    height, width = shape 
    matrix = np.zeros(shape)
    for n, (i,j) in enumerate(zig_zag(height, width)):
        matrix[i,j] = array[n]
    return matrix




def zig_zag(height, width):
    i,j = 0,0
    direction = 1 

    yield i,j
    
    for n in range(width*height - 1):
        going_up = (direction == 1)

        if going_up and j == width-1:
            i += 1 
            direction = -direction
        elif going_up and i == 0:
            j += 1
            direction = -direction
        elif not going_up and i == height-1:
            j += 1
            direction = -direction
        elif not going_up and j == 0:
            i += 1 
            direction = -direction
        else:
            i -= direction
            j += direction
        
        yield i,j


def transform(matrix, quality=1):
    vector = np.array([matrix[i,j] for i,j in zig_zag(*matrix.shape)])
    size = len(vector)

    result = dct(vector)
    for i in range(size):
        result[i] //= 1 + quality * i
    return result

def distransform(vector, shape, quality=1):
    size = len(vector)
    result = vector
    
    for i in range(size):
        result[i] *= 1 + quality * i 

    result[0] /= 2 
    result = idct(result) * 2 / size

    matrix = np.zeros(shape=shape)
    for n, (i,j) in zip(range(size), zig_zag(*shape)):
        matrix[i,j] = result[n]

    return matrix