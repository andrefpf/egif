import numpy as np 


def dwt(array, iterations=1):
    '''
        Get an array and apply dwt over it. 

        The main idea here is that in the left part of the array we put the
        even indexed elements, and in the right part we put only the difference
        between these and their adjacent pixels. This separates the image in 
        core parts and details, and the details are usually small number like 0
        and this makes the compression much more efficient. The same process is 
        applied over and over on the left part of the array.
    '''

    if len(array) % 2 != 0:
        raise ValueError('The size of the array is not multiple of 2')

    half = len(array) // 2
    array = np.array(array, dtype=int)
    result = np.zeros(half*2, dtype=int)

    result[:half] = array[::2]
    result[half:] = array[1::2] - array[::2]

    if iterations > 1:
        result[:half] = dwt(result[:half], iterations-1)
        
    return result


def idwt(array, iterations=1):
    '''
        Get a dwt transformed array and returns the original one.

        To make this we just need to start on the left part and the even 
        indexed arrays will be the left part of the input, and the odd 
        indexed will be the left part plus the right one.
    '''

    if len(array) % 2 != 0:
        return array

    half = len(array) // 2
    array = np.array(array, dtype=int)
    result = np.zeros(half*2, dtype=int)

    if iterations > 1:
        array[:half] = idwt(array[:half], iterations-1)

    result[::2]  = array[:half]
    result[1::2] = array[:half] + array[half:]
    
    return result

def dwt_2d(matrix, iterations=1):
    '''
        Get a matrix and apply a dwt in both directions.
    '''

    h, w = matrix.shape
    result = np.zeros((h, w)) 

    for i in range(h):
        result[i] = dwt(matrix[i], iterations)
    
    for j in range(w):
        result[:, j] = dwt(result[:, j], iterations)
    
    return result

def idwt_2d(matrix, iterations=1):
    '''
        Get a dwt transformed matrix and returns the original one.
    '''
    h, w = matrix.shape
    result = np.zeros((h, w))

    for i in range(h):
        result[i] = idwt(matrix[i], iterations)

    for j in range(w):
        result[:, j] = idwt(result[:, j], iterations)
    
    return result

def truncate(matrix, details=0.95, iterations=1):
    '''
        Remove unecessary details from a transformed matrix. 
    '''
    h, w = matrix.shape
    result = np.zeros((h,w))

    while iterations > 0:
        htemp = h >> iterations
        wtemp = w >> iterations
        threshold = (1-details) * 256 / (iterations * 8)

        for i in range(htemp):
            for j in range(wtemp):
                if abs(matrix[i, j+wtemp]) < threshold:
                    matrix[i, j+wtemp] = 0

                if abs(matrix[i + htemp, j]) < threshold:
                    matrix[i + htemp, j] = 0
                    
                if abs(matrix[i + htemp, j + wtemp]) < threshold:
                    matrix[i + htemp, j + wtemp] = 0

        iterations -= 1
