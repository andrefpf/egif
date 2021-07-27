import numpy as np 


def dwt(array, levels=1):
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
        raise ValueError(f'The size of the array ({len(array)}) is not multiple of 2')

    half = len(array) // 2
    array = np.array(array, dtype=int)
    result = np.zeros(half*2, dtype=int)

    result[:half] = array[::2]
    result[half:] = array[1::2] - array[::2]

    if levels > 1:
        result[:half] = dwt(result[:half], levels-1)
        
    return result


def idwt(array, levels=1):
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

    if levels > 1:
        array[:half] = idwt(array[:half], levels-1)

    result[::2]  = array[:half]
    result[1::2] = array[:half] + array[half:]
    
    return result

def dwt_2d(matrix, levels=1):
    '''
        Get a 2d matrix and apply a dwt in both directions.
    '''

    h, w = matrix.shape
    result = np.zeros((h, w)) 

    for i in range(h):
        result[i] = dwt(matrix[i], levels)
    
    for j in range(w):
        result[:, j] = dwt(result[:, j], levels)
    
    return result

def idwt_2d(matrix, levels=1):
    '''
        Get a dwt transformed 2d matrix and returns the original one.
    '''
    h, w = matrix.shape
    result = np.zeros((h, w))

    for i in range(h):
        result[i] = idwt(matrix[i], levels)

    for j in range(w):
        result[:, j] = idwt(result[:, j], levels)
    
    return result

def dwt_3d(matrix, levels=1):
    '''
        Get a 2d matrix and apply a dwt in both directions.
    '''

    f, h, w = matrix.shape
    result = matrix.copy()

    # transform frames
    for k in range(f):
        result[k] = dwt_2d(result[k], levels)
    
    # transform time
    for i in range(h >> levels):
        for j in range(w >> levels):
            result[:,i,j] = dwt(result[:,i,j], levels)
    
    return result

def idwt_3d(matrix, levels=1):
    '''
        Get a dwt transformed 2d matrix and returns the original one.
    '''

    f, h, w = matrix.shape
    result = matrix.copy()
    
    # transform time
    for i in range(h >> levels):
        for j in range(w >> levels):
            result[:,i,j] = idwt(result[:,i,j], levels)

    # transform frames
    for k in range(f):
        result[k] = idwt_2d(result[k], levels)
    
    return result

def truncate(matrix, details=0.95, levels=1):
    '''
        Remove unecessary details from a transformed matrix. 
    '''
    h, w = matrix.shape

    while levels > 0:
        htemp = h >> levels
        wtemp = w >> levels
        threshold = (1-details) * 256 / (levels * 8)

        for i in range(htemp):
            for j in range(wtemp):
                # upper right
                if abs(matrix[i, j+wtemp]) < threshold:
                    matrix[i, j+wtemp] = 0
                
                # lower left
                if abs(matrix[i + htemp, j]) < threshold:
                    matrix[i + htemp, j] = 0
                
                # lower right 
                if abs(matrix[i + htemp, j + wtemp]) < threshold:
                    matrix[i + htemp, j + wtemp] = 0
        levels -= 1
    return matrix

def truncate2(matrix, details=0.95, levels=1):
    h, w = matrix.shape

    result = np.zeros((h,w))

    maxi = h >> levels
    maxj = w >> levels

    hlog = 0
    wlog = 0

    for i in range(h):
        for j in range(w):
            if i > maxi:
                hlog += 1
                maxi *= 2

            if j > maxj:
                wlog += 1
                maxj *= 2

            level = max(hlog, wlog)
            threshold = level * (10 - details)

            if abs(matrix[i,j]) < threshold:
                matrix[i,j] = 0
            else:
                matrix[i,j] = matrix[i,j]

        maxj = w >> levels
        wlog = 0

    return matrix

def constrain(matrix, mini, maxi):
    h, w = matrix.shape
    
    for i in range(h):
        for j in range(w):
            if matrix[i,j] < mini:
                matrix[i,j] = mini

            if matrix[i,j] > maxi:
                matrix[i,j] = maxi