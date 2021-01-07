import numpy as np
from time import time

from egif.image import load_image
from egif.compression import compress_2d, decompress_2d, compress_3d, decompress_3d
from egif.renderer import show_image, compare_images


def gradient_example():
    original = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            original[i,j] = (i+j) * 10
    
    compressed = compress_2d(original)
    decompressed = decompress_2d(compressed)

    differences = np.sum(np.abs(original - decompressed))
    print('total differences', differences)
    print()

    compare_images(original, decompressed)


def shrek_2d_example():
    path = 'examples/small/0.jpg'

    original = load_image(path)
    a = time()
    compressed = compress_2d(original)
    b = time()
    decompressed = decompress_2d(compressed)
    c = time()

    print('time to compress', b-a)
    print('time to decompress', c-b)
    print()

    compare_images(original, decompressed)


def lusca_2d_example():
    path = 'examples/high/0.jpg'

    original = load_image(path, (1280, 720))
    a = time()
    compressed = compress_2d(original)
    b = time()
    decompressed = decompress_2d(compressed)
    c = time()

    print('time to compress', b-a)
    print('time to decompress', c-b)
    print()

    compare_images(original, decompressed)


def shrek_3d_example():
    images = []
    for i in range(8):
        path = f'examples/small/{i}.jpg'
        img = load_image(path)
        images.append(img)
    
    original = np.stack(images)
    a = time()
    compressed = compress_3d(original)
    b = time()
    decompressed = decompress_3d(compressed)
    c = time()
    
    print('time to compress', b-a)
    print('time to decompress', c-b)
    print()

    for org, dcp in zip(original, decompressed):
        compare_images(org, dcp)


def walking_3d_example():
    images = []
    for i in range(8):
        path = f'examples/medium/{i}.jpg'
        img = load_image(path)
        images.append(img)
    
    original = np.stack(images)
    a = time()
    compressed = compress_3d(original)
    b = time()
    decompressed = decompress_3d(compressed)
    c = time()
    
    print('time to compress', b-a)
    print('time to decompress', c-b)
    print()

    for org, dcp in zip(original, decompressed):
        compare_images(org, dcp)
    

gradient_example()
shrek_2d_example()
lusca_2d_example()
shrek_3d_example()
walking_3d_example()