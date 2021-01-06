import numpy as np
from math import cos, pi, sqrt

from scipy import fft

from .utils import sigmoid

# this code is not very pythonic, because i wrote
# it thinking in how to rewrite it in c++

COS45 = sqrt(2)/2

def dct(vector):
    n = len(vector)

    if n == 1:
        return vector

    if (n == 0) or (n % 2 != 0):
        raise ValueError('Vector size is not a power of 2.')

    alpha = np.zeros(n//2)
    beta = np.zeros(n//2)
    result = np.zeros(n)   

    for i in range(n//2):
        c = np.cos((0.5 + i) * np.pi / n) * 2
        alpha[i] = (vector[i] + vector[n - i - 1])
        beta[i] = (vector[i] - vector[n - i - 1]) / c 
        
    trans_alpha = dct(alpha)
    trans_beta = dct(beta)

    for i in range(n//2 - 1):
        result[2*i] = trans_alpha[i]
        result[2*i + 1] = trans_beta[i] + trans_beta[i+1]
    result[n-2] = trans_alpha[n//2-1]
    result[n-1] = trans_beta[n//2-1]
    return result
    

def fdct(vector):
    n = len(vector)

    if n == 2:
        a = vector[0] + vector[1]
        b = (vector[0] - vector[1]) * COS45
        vector[0], vector[1] = a,b
        return vector
    elif not any(vector):
        return vector
    elif (n & 1) or (n == 0):
        raise ValueError('Vector size is not a power of 2.')

    alpha = np.zeros(n//2)
    beta = np.zeros(n//2)

    for i in range(n//2):
        c = cos((0.5 + i) * pi / n) * 2
        alpha[i] = (vector[i] + vector[n - i - 1])
        beta[i] = (vector[i] - vector[n - i - 1]) / c

    fdct(alpha)
    fdct(beta)

    for i in range(n//2 - 1):
        vector[2*i] = alpha[i]
        vector[2*i + 1] = beta[i] + beta[i+1]
    vector[n-2] = alpha[n//2-1]
    vector[n-1] = beta[n//2-1]
    return vector


def idct(vector):
    # before call it you should divide the first value by two
    # after call it you should multiply all the values by 2/N
    # where N is the size of the array

    n = len(vector)

    if n == 1:
        return vector
    elif not any(vector):
        return vector

    if (n == 0) or (n % 2 != 0):
        raise ValueError('Vector size is not a power of 2.')

    alpha = np.zeros(n//2)
    beta = np.zeros(n//2)
    result = np.zeros(n)   

    alpha[0] = vector[0]
    beta[0] = vector[1]
    for i in range(1, n//2):
        alpha[i] = vector[2*i]
        beta[i] = vector[2*i - 1] + vector[2*i + 1]

    trans_alpha = idct(alpha)
    trans_beta = idct(beta)

    for i in range(n//2): 
        c = np.cos((0.5 + i) * np.pi / n) * 2
        result[i] = trans_alpha[i] + trans_beta[i] / c
        result[n - i -1] = trans_alpha[i] - trans_beta[i] / c
    return result


# dct type IV are not used here, but i think it is beautifull 
def dct_IV(x):
    N = len(x)
    X = np.zeros(N)
    for k in range(N):
        s = 0
        for n in range(N):
            s += x[n] * np.cos(np.pi/N * (n + 1/2) * (k + 1/2))
        X[k] = s
    return X

def idct_IV(x):
    N = len(x)
    X = dct(x)
    return X * 2/N


def dct_2d(matrix):
    h,w = matrix.shape

    for i in range(h):
        # matrix[i] = dct(matrix[i])
        fdct(matrix[i])
        # matrix[i] = fft.dct(matrix[i])


    for j in range(w):
        # matrix[:, j] = dct(matrix[:, j])
        fdct(matrix[:, j])
        # matrix[:, j] = fft.dct(matrix[:, j])

    return matrix

def idct_2d(matrix):
    h,w = matrix.shape

    for j in range(w):
        # matrix[:, j] = fft.idct(matrix[:, j])
        matrix[0, j] /= 2
        matrix[:, j] = idct(matrix[:, j]) * 2 / h

    for i in range(h):
        # matrix[i] = fft.idct(matrix[i])
        matrix[i, 0] /= 2
        matrix[i] = idct(matrix[i]) * 2 / w

    return matrix


def dct_3d(matrix):
    l,h,w = matrix.shape

    for k in range(l):
        matrix[k] = dct_2d(matrix[k])

    for i in range(h): 
        for j in range(w):
            matrix[:, i, j] = fdct(matrix[:, i, j])

    return matrix

def idct_3d(matrix):
    l,h,w = matrix.shape

    for i in range(h):
        for j in range(w):
            matrix[0, i, j] /= 2
            matrix[:, i, j] = idct(matrix[:, i, j]) * 2 / l
    
    for k in range(l):
        matrix[k] = idct_2d(matrix[k])

    return matrix


# ises = [0,0,1,2,1,0,0,1]
# jotes = [0,1,0,0,1,2,3,2]
