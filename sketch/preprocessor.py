import numpy as np 
from PIL import Image
import pathlib


KR = 0.299
KG = 0.587
KB = 0.114


def load_images(paths):
    images = []
    for path in paths:
        img = Image.open(path)
        frame = np.asarray(img)
        rgb = (frame[:,:,0], frame[:,:,1], frame[:,:,2])
        images.append(rgb)
    return images

def load_folder(path, formats=None):
    paths = []
    for p in pathlib.Path(path).iterdir():
        if p.is_file() and (formats is None or p.suffix in formats):
            paths.append(p)
    return load_images(paths)

def correct_dimentions(matrix, iterations=4):
    h, w = matrix.shape 
    h -= h % iterations
    w -= w % iterations

    result = matrix[:h, :w].copy()     
    return result

def merge_matrices(a, b):
    h, w = a.shape
    merged = np.zeros((h,w))
    merged[0:h:2, :] = a[0:h:2, :]
    merged[1:h:2, :] = b[1:h:2, :]
    return merged

def rgb_to_ycbcr(R, G, B):
    h, w = R.shape

    Y = np.zeros((h,w))
    Cb = np.zeros((h,w))
    Cr = np.zeros((h,w))

    for i in range(h):
        for j in range(w):
            r = R[i,j]
            g = G[i,j]
            b = B[i,j]
            
            y = (KR*r + KG*g + KB*b)
            cb = (b - y) / (1 - KB) / 2
            cr = (r - y) / (1 - KR) / 2

            Y[i,j] = Y
            Cb[i,j] = cb
            Cr[i,j] = cr 
            
    return (Y, Cb, Cr)

def ycbcr_to_rgb(Y, Cb, Cr):
    h, w = Y.shape

    R = np.zeros((h,w))
    G = np.zeros((h,w))
    B = np.zeros((h,w))

    for i in range(h):
        for j in range(w):
            y = Y[i,j]
            cb = Cb[i,j]
            cr = Cr[i,j]

            r = y + (2 - 2 * KR) * cr
            g = y - (2 - 2 * KB) * cb * KB/KR - (2 - 2*KR) * cr * KR/KG
            b = y + (2 - 2 * KB) * cb

            R[i,j] = r
            G[i,j] = g 
            B[i,j] = b

    return R, G, B

