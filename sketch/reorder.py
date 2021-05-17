import numpy as np 


def unroll(matrix, iterations):
    h, w = matrix.shape
    array = np.zeros(h*w, dtype=int)
    k = 0

    htemp = h >> iterations
    wtemp = w >> iterations

    for i in range(htemp):
        for j in range(wtemp):
            array[k] = matrix[i, j]
            k += 1

    while iterations > 0:
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

        iterations -= 1
        htemp = h >> iterations
        wtemp = w >> iterations

    return array

def roll(array, shape, iterations):
    h, w = shape
    matrix = np.zeros((h, w), dtype=int)
    k = 0

    htemp = h >> iterations
    wtemp = w >> iterations

    for i in range(htemp):
        for j in range(wtemp):
            matrix[i, j] = array[k]
            k += 1

    while iterations > 0:
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

        iterations -= 1
        htemp = h >> iterations
        wtemp = w >> iterations

    return matrix
