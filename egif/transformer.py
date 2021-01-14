import numpy as np
from math import cos, pi, sqrt

from scipy import fft

from .utils import is_pow_2

# this code is not very pythonic, because i wrote
# it thinking in how to rewrite it in c++


class DCT:
    SQRT_2 = 1.4142135623730951

    def __init__(self, size=8):
        if not is_pow_2(size):
            raise ValueError('Array size is not a power of 2.')

        self.size = size
        # self.cossines = [cos(i) for i in range(n) for j in range(size)]
        # im too dumb to do it a simple way
    
    def foward(self, array, copy=False):
        if len(array) != self.size:
            raise ValueError('Array size is not equal the predefined.')

        if copy:
            array = array.copy()

        return self._fdct(array)

    def inverse(self, array, copy=False):
        if len(array) != self.size:
            raise ValueError('Array size is not equal the predefined.')

        if copy:
            array = array.copy()

        array[0] /= 2
        return self._ifdct(array) * 2 // self.size

    # def get_cos(self, i, n):
    #     return self.cossines[i + n//2 - 1] 

    def _fdct(self, array):
        # unscaled algorithm

        n = len(array)

        if n == 2:
            a = array[0] + array[1]
            b = (array[0] - array[1]) * self.SQRT_2 / 2
            array[0], array[1] = a,b
            return array
        elif not any(array):  # dct([0,0,0,0]) == [0,0,0,0]
            return array

        alpha = np.zeros(n//2)
        beta = np.zeros(n//2)

        for i in range(n//2):
            c = cos((0.5 + i) * pi / n) * 2
            
            alpha[i] = (array[i] + array[n - i - 1])
            beta[i] = (array[i] - array[n - i - 1]) / c

        self._fdct(alpha)
        self._fdct(beta)

        for i in range(n//2 - 1):
            array[2*i] = alpha[i]
            array[2*i + 1] = beta[i] + beta[i+1]
        array[n-2] = alpha[n//2-1]
        array[n-1] = beta[n//2-1]
        return array

    
    def _ifdct(self, array):
        # unscaled algorithm 
        
        n = len(array)

        if n == 2:
            a = array[0] + (array[1] / self.SQRT_2)
            b = array[0] - (array[1] / self.SQRT_2)
            array[0], array[1] = a,b
            return array
        elif not any(array):
            return array

        alpha = np.zeros(n//2)
        beta = np.zeros(n//2)

        alpha[0] = array[0]
        beta[0] = array[1]
        for i in range(1, n//2):
            alpha[i] = array[2*i]
            beta[i] = array[2*i - 1] + array[2*i + 1]

        self._ifdct(alpha)
        self._ifdct(beta)

        for i in range(n//2):
            c = cos((0.5 + i) * pi / n) * 2
            array[i] = alpha[i] + (beta[i] / c)
            array[n - i -1] = alpha[i] - (beta[i] / c)
        return array



class DCT2D(DCT):
    def __init__(self, width, height):
        if not is_pow_2(width):
            raise ValueError('Matrix width is not a power of 2.')

        if not is_pow_2(height):
            raise ValueError('Matrix height is not a power of 2.')

        self.width = width
        self.height = height
    

    def foward(self, matrix):
        right_shape = all([
            matrix.shape[0] == self.height,
            matrix.shape[1] == self.width,
        ])

        if not right_shape:
            raise ValueError('Matrix size is not equal the predefined size.')

        for h in range(self.height):
            self._fdct(matrix[h, :])

        for w in range(self.width):
            self._fdct(matrix[:, w])

        return matrix

    def inverse(self, matrix):
        right_shape = all([
            matrix.shape[0] == self.height,
            matrix.shape[1] == self.width,
        ])

        if not right_shape:
            raise ValueError('Matrix size is not equal the predefined size.')

        for w in range(self.width):
            matrix[0, w] /= 2
            matrix[:, w] = self._ifdct(matrix[:, w]) * 2 / self.height

        for h in range(self.height):
            matrix[h, 0] /= 2
            matrix[h, :] = self._ifdct(matrix[h, :]) * 2 / self.width

        return matrix



class DCT3D(DCT):
    def __init__(self, width, height, length):
        if not is_pow_2(width):
            raise ValueError('Matrix width is not a power of 2.')

        if not is_pow_2(height):
            raise ValueError('Matrix height is not a power of 2.')

        if not is_pow_2(length):
            raise ValueError('Matrix length is not a power of 2.')

        self.width = width
        self.height = height
        self.length = length
    

    def foward(self, matrix):
        right_shape = all([
            matrix.shape[0] == self.length,
            matrix.shape[1] == self.height,
            matrix.shape[2] == self.width,
        ])

        if not right_shape:
            raise ValueError('Matrix size is not equal the predefined size.')
        
        # transform over x axis
        for l in range(self.length):
            for w in range(self.width):
                self._fdct(matrix[l, :, w])
        
        # transform over y axis
        for l in range(self.length):
            for h in range(self.height):
                self._fdct(matrix[l, h, :])

        # transform over z axis
        for h in range(self.height):
            for w in range(self.width):
                self._fdct(matrix[:, h, w])
        
        return matrix
                

    def inverse(self, matrix):
        right_shape = all([
            matrix.shape[0] == self.length,
            matrix.shape[1] == self.height,
            matrix.shape[2] == self.width,
        ])

        if not right_shape:
            raise ValueError('Matrix size is not equal the predefined size.')

        # transform over z axis
        for h in range(self.height):
            for w in range(self.width):
                matrix[0, h, w] /= 2
                matrix[:, h, w] = self._ifdct(matrix[:, h, w]) * 2 / self.length

        # transform over y axis
        for l in range(self.length):
            for h in range(self.height):
                matrix[l, h, 0] /= 2
                matrix[l, h, :] = self._ifdct(matrix[l, h, :]) * 2 / self.width
        
        # transform over x axis
        for l in range(self.length):
            for w in range(self.width):
                matrix[l, 0, w] /= 2
                matrix[l, :, w] = self._ifdct(matrix[l, :, w]) * 2 / self.height
                
        return matrix
