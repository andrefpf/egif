import numpy as np
from matplotlib import pyplot as plt 
from PIL import Image
from time import time

from egif import image, dct, encoding


# bad compression
# QUANTIZATION_TABLE = np.array([[1+i+j for i in range(8)] for j in range(8)]) 

# good quality, good compression 
QUANTIZATION_TABLE = np.array([
    [16, 11, 10, 16, 24,  40,  51,  61],
    [12, 12, 14, 19, 26,  58,  60,  55],
    [14, 13, 16, 24, 40,  57,  69,  56],
    [14, 17, 22, 29, 51,  87,  80,  62],
    [18, 22, 37, 56, 68,  109, 103, 77],
    [24, 35, 55, 64, 81,  104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

# =3 
sig_moide = lambda x: 1 / (1 + 2**x)
a = 100
TESTE = np.array([[-sig_moide(i+j-8)*a + 200 for i in range(8)] for j in range(8)])
QUANTIZATION_TABLE = TESTE.astype(int)



# print((QUANTIZATION_TABLE - TESTE).astype(int))


# fig = plt.figure()
# ax = fig.add_subplot(1, 2, 1)
# imgplot = plt.imshow(QUANTIZATION_TABLE, vmin=0, vmax=255, cmap='gray')
# ax.set_title('DEFAULT')

# ax = fig.add_subplot(1, 2, 2)
# imgplot = plt.imshow(TESTE, vmin=0, vmax=255, cmap='gray')
# ax.set_title('ALFORITHM')

# plt.show()


def trans(matrix):
    height, width = matrix.shape
    vector = np.zeros(height*width)

    n = 8
    
    pos = 0
    for i in range(0, height, n):
        for j in range(0, width, n):
            t = matrix[i:i+n, j:j+n]
            vector[pos : pos+n*n] = image.transform(t)
            pos += n*n
    return vector

def distrans(vector, shape):
    height, width = shape
    matrix = np.zeros((height, width))

    n = 8

    pos = 0
    for i in range(0, height, n):
        for j in range(0, width, n):
            t = vector[pos : pos+n*n]
            matrix[i:i+n, j:j+n] = image.distransform(t, (n,n))
            pos += n*n
    return matrix



def trans2(matrix):
    h,w = matrix.shape
    vector = np.zeros(w*h)

    for n, (i,j) in enumerate(image.zig_zag(h,w)):
        vector[n] = matrix[i,j]
    
    for i in range(0, len(vector), 64):
        vector[i : i+64] = dct.transform(vector[i : i+64])

    return vector

def distrans2(vector, shape):
    matrix = np.zeros(shape, dtype=int)
    array = np.zeros(len(vector))

    for i in range(0, len(vector), 64):
        array[i : i+64] = dct.distransform(vector[i : i+64])   

    for n, (i,j) in enumerate(image.zig_zag(*shape)):
        matrix[i,j] = array[n]

    return matrix

def trans3(matrix):
    h,w = matrix.shape
    new_matrix = np.zeros((h,w))

    for i in range(h):
        for j in range(0, w, 8):
            new_matrix[i, j:j+8] = dct.transform(matrix[i, j:j+8], 2)

    for i in range(w):
        for j in range(0, h, 8):
            new_matrix[j:j+8, i] = dct.transform(new_matrix[j:j+8, i], 2)

    return new_matrix

def distrans3(matrix, ignoreit):
    h,w = matrix.shape
    new_matrix = np.zeros((h,w))

    for i in range(w):
        for j in range(0, h, 8):
            new_matrix[j:j+8, i] = dct.distransform(matrix[j:j+8, i], 2)

    for i in range(h):
        for j in range(0, w, 8):
            new_matrix[i, j:j+8] = dct.distransform(new_matrix[i, j:j+8], 2)

    return new_matrix


def trans4(matrix):
    h,w = matrix.shape
    transformed_matrix = matrix.copy()

    # dct
    for i in range(h):
        for j in range(0, w, 8):
            transformed_matrix[i, j:j+8] = dct.dct(transformed_matrix[i, j:j+8])
    
    for i in range(0, h, 8):
        for j in range(w):
            transformed_matrix[i:i+8, j] = dct.dct(transformed_matrix[i:i+8, j])

    # # quantization
    # q = np.tile(QUANTIZATION_TABLE, (h//8, w//8))
    # transformed_matrix = np.round(transformed_matrix / q)
    
    return transformed_matrix 

def distrans4(matrix, ignoreit=None):
    h,w = matrix.shape
    transformed_matrix = matrix.copy()

    # # disquantization 
    # transformed_matrix *= np.tile(QUANTIZATION_TABLE, (h//8, w//8))

    # idct
    for i in range(0, h, 8):
        for j in range(w):
            t = transformed_matrix[i:i+8, j]
            t[0] /= 2
            transformed_matrix[i:i+8, j] = dct.idct(t) * 2 / 8

    for i in range(h):
        for j in range(0, w, 8):
            t = transformed_matrix[i, j:j+8]
            t[0] /= 2
            transformed_matrix[i, j:j+8] = dct.idct(t) * 2 / 8

    return transformed_matrix

def trans5(matrix):
    h,w = matrix.shape
    transformed_matrix = matrix.copy()

    chunk = 8

    for i in range(0, h, chunk):
        for j in range(0, w, chunk):
            dct.dct_2d(transformed_matrix[i:i+chunk, j:j+chunk])

    return transformed_matrix

def distrans5(matrix):
    h,w = matrix.shape
    distransformed_matrix = matrix.copy()

    chunk = 8

    for i in range(0, h, chunk):
        for j in range(0, w, chunk):
            dct.idct_2d(distransformed_matrix[i:i+chunk, j:j+chunk])

    return distransformed_matrix



def example_shrek():
    for i in range(6):
        img = Image.open(f'examples/small/{i}.jpg').convert('L')
        matrix = np.asarray(img, dtype=int)

        a = time()
        transformed = trans4(matrix)
        b = time()
        distransformed = distrans4(transformed, matrix.shape)
        c = time()

        print(b-a, c-b)

        fig = plt.figure()
        ax = fig.add_subplot(1, 2, 1)
        imgplot = plt.imshow(matrix, vmin=0, vmax=255, cmap='gray')
        ax.set_title('Before')

        ax = fig.add_subplot(1, 2, 2)
        imgplot = plt.imshow(distransformed, vmin=0, vmax=255, cmap='gray')
        ax.set_title('After')

        plt.show()


def example_lusca():
    for i in range(2):
        img = Image.open(f'examples/high/{i}.jpg').convert('L').resize((1280,720))
        matrix = np.asarray(img, dtype=int)

        a = time()
        transformed = trans4(matrix)
        b = time()
        distransformed = distrans4(transformed, matrix.shape)
        c = time()

        print(b-a, c-b)

        fig = plt.figure()
        ax = fig.add_subplot(1, 2, 1)
        imgplot = plt.imshow(matrix, vmin=0, vmax=255, cmap='gray')
        ax.set_title('Before')

        ax = fig.add_subplot(1, 2, 2)
        imgplot = plt.imshow(distransformed, vmin=0, vmax=255, cmap='gray')
        ax.set_title('After')

        plt.show()


def example_gradient():
    matrix = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            matrix[i,j] = (i+j) * 10
            
    transformed = trans5(matrix)
    distransformed = distrans5(transformed)

    assert np.allclose(distransformed, distransformed)

    fig = plt.figure()
    ax = fig.add_subplot(1, 3, 1)
    imgplot = plt.imshow(matrix, vmin=0, vmax=255, cmap='gray')
    ax.set_title('Original')

    ax = fig.add_subplot(1, 3, 2)
    imgplot = plt.imshow(transformed, cmap='gray')
    ax.set_title('Transformed')

    ax = fig.add_subplot(1, 3, 3)
    imgplot = plt.imshow(distransformed, vmin=0, vmax=255, cmap='gray')
    ax.set_title('Distransformed')

    plt.show()

def example_file():
    img = Image.open('examples/high/0.jpg').convert('L').resize((1080, 720))
    matrix = np.asarray(img, dtype=int)
    transformed = trans4(matrix).astype(int)


    gambiarra = transformed.flatten()
    signal = np.array([(1 if i>=0 else -1) for i in gambiarra])
    gambiarra = np.abs(gambiarra)

    encoded = encoding.encode(gambiarra)

    with open('test.egif', 'wb') as f:
        f.write(encoded)
    
    with open('test.egif', 'rb') as f:
        recovered = encoding.decode(f.read())
        assert np.allclose(recovered, gambiarra)
        recovered = np.array(recovered) * signal

    recovered = recovered.reshape(matrix.shape)
    assert np.allclose(recovered, transformed)
    

    distransformed = distrans4(recovered, recovered.shape)

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(matrix, vmin=0, vmax=255, cmap='gray')
    ax.set_title('Before')

    ax = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(distransformed, vmin=0, vmax=255, cmap='gray')
    ax.set_title('After')

    plt.show()






example_shrek()
# example_lusca()
# example_gradient()
# example_file()

# print('Importou')

# print('Tansformou')

# tamanho_original = len(matrix.flatten()) * 8
# tamanho_transformado = len(transformed.flatten()) * 16
# tamanho_comprimido = len(code) * 16


# print('tamanho original', tamanho_original)
# print('tamanho transformado', tamanho_transformado)
# print('tamanho comprimido', tamanho_comprimido)
# print('taxa de compressão', tamanho_original/tamanho_comprimido)






