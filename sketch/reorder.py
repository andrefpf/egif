import numpy as np 


def unroll(matrix, levels):
    h, w = matrix.shape
    array = np.zeros(h*w, dtype=int)
    k = 0

    htemp = h >> levels
    wtemp = w >> levels

    for i in range(htemp):
        for j in range(wtemp):
            array[k] = matrix[i, j]
            k += 1

    while levels > 0:
        for i in range(htemp):
            for j in range(wtemp):
                array[k] = matrix[i, j + wtemp]
                k += 1
        
        for i in range(htemp):
            for j in range(wtemp):
                array[k] = matrix[i + htemp, j]
                k += 1

        for i in range(htemp):
            for j in range(wtemp):
                array[k] = matrix[i + htemp, j + wtemp]
                k += 1

        levels -= 1
        htemp = h >> levels
        wtemp = w >> levels

    return array

def roll(array, shape, levels):
    h, w = shape
    matrix = np.zeros((h, w), dtype=int)
    k = 0

    htemp = h >> levels
    wtemp = w >> levels

    for i in range(htemp):
        for j in range(wtemp):
            matrix[i, j] = array[k]
            k += 1

    while levels > 0:
        for i in range(htemp):
            for j in range(wtemp):
                matrix[i, j + wtemp] = array[k]
                k += 1
        
        for i in range(htemp):
            for j in range(wtemp):
                matrix[i + htemp, j] = array[k]
                k += 1

        for i in range(htemp):
            for j in range(wtemp):
                matrix[i + htemp, j + wtemp] = array[k]
                k += 1

        levels -= 1
        htemp = h >> levels
        wtemp = w >> levels

    return matrix
