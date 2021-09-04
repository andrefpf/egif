from time import time
import numpy as np
from scipy.fft import dct
import matplotlib.pyplot as plt
from PIL import Image
from dahuffman import HuffmanCodec

from sketch import reorder
from sketch import transformer
from sketch import preprocessor
from sketch import egif 


def load_img(path):
    img = Image.open(path)
    # img = img.convert('YCbCr')
    frame = np.asarray(img)
    r = frame[:,:,0]
    g = frame[:,:,1]
    b = frame[:,:,2]
    return r,g,b

def show_image(matrix):
    plt.imshow(matrix, vmin=0, vmax=255, cmap='gray')
    plt.show()

def show_rgb(matrix):
    rgb = np.moveaxis(matrix, [0,1,2], [2,0,1])
    show_image(rgb)

def compare_rgb(matrix_a, matrix_b):
    rgb_a = np.moveaxis(matrix_a, [0,1,2], [2,0,1])
    rgb_b = np.moveaxis(matrix_b, [0,1,2], [2,0,1])
    compare_images(rgb_a, rgb_b)

def compare_images(matrix_a, matrix_b):
    fig = plt.figure()

    ax = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(matrix_a, vmin=0, vmax=255, cmap='gray')

    ax = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(matrix_b, vmin=0, vmax=255, cmap='gray')

    plt.show()

def denoise(matrix, details=0.95):
    height, width = matrix.shape

    remap = lambda x, max1, max2: x * max2 / max1

    for i in range(height):
        for j in range(width):
            if (i <= (height >> ITERS) and j <= (width >> ITERS)):
                continue

            threshold = 1 - details
            scale = (i+j) * 64 / (height + width)

            if (abs(matrix[i,j]) < scale * threshold):
                matrix[i,j] = 0

def compress_data(data):
    freq = dict()

    for i in data:
        freq.setdefault(i, 0)
        freq[i] += 1
    
    codec = HuffmanCodec.from_frequencies(freq)
    return codec.encode(data)

def run_length_encode(data):
    result = []

    repetitions = 0

    for i in data:
        if (i == 0):
            repetitions += 1
        elif (repetitions != 0):
            result.append(0)
            result.append(repetitions)
            repetitions = 0
        else:
            result.append(i)
    
    return np.array(result)

def mse(a, b):
    assert a.shape == b.shape
    h, w = a.shape
    return np.sum((a-b)*(a-b) / h / w)

def test_transforms():
    level = 4
    paths = [f'../egif_datasets/bird/bird_{i}.png' for i in range(1)]
    image = preprocessor.load_images(paths)[0]
    compressed = np.copy(image)

    egif.rgb_to_ycocg(compressed)
    egif.dwt_2d(compressed[0], level)
    egif.dwt_2d(compressed[1], level)
    egif.dwt_2d(compressed[2], level)

    egif.truncate(compressed[0], 4, 2)
    egif.truncate(compressed[1], 10, 4)
    egif.truncate(compressed[2], 10, 4)

    compressed_data = compress_data(run_length_encode(compressed.flatten()))
    original_size = image.shape[0] * image.shape[1] * image.shape[2]
    compressed_size = len(compressed_data)

    print('original size:', original_size)
    print('compressed size:', compressed_size)
    print('compression rate:', original_size / compressed_size)

    decompressed = np.copy(compressed)

    egif.idwt_2d(decompressed[0], level)
    egif.idwt_2d(decompressed[1], level)
    egif.idwt_2d(decompressed[2], level)
    egif.ycocg_to_rgb(decompressed)

    print('mse:', mse(image[0], decompressed[0]))

    show_image(compressed[0])
    compare_rgb(image, decompressed)





