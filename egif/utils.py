import numpy as np

def sigmoid(x):
    return 1 / (1 + 2**x)

def is_pow_2(x):
    # it is a bit manipulation hack 
    # if x = 8 = 1000
    # then x-1 = 7 = 0111
    # then 1000 and 0111 = 0
    return (x != 0) and (x & (x-1) == 0)

def chunks_2d(matrix, size=8):
    height, width = matrix.shape
    for h in range(0, height, size):
        for w in range(0, width, size):
            yield matrix[h:h+size, w:w+size]

def chunks_3d(matrix, size=8):
    lenght, height, width = matrix.shape
    for l in range(0, lenght, size):
        for h in range(0, height, size):
            for w in range(0, width, size):
                yield matrix[l:l+size, h:h+size, w:w+size]

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