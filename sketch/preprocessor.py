import numpy as np 
from PIL import Image
import pathlib


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

def correct_dimentions(matrix, levels=4):
    h, w = matrix.shape 
    h -= h % (1 << levels)
    w -= w % (1 << levels)
    result = matrix[:h, :w].copy()     
    return result

def merge_matrices(a, b):
    h, w = a.shape
    merged = np.zeros((h,w))
    merged[0:h:2, :] = a[0:h:2, :]
    merged[1:h:2, :] = b[1:h:2, :]
    return merged

def rgb_to_ycbcr(r, g, b):
    h, w = r.shape

    y = np.zeros((h,w))
    cb = np.zeros((h,w))
    cr = np.zeros((h,w))

    for i in range(h):
        for j in range(w):
            y[i,j]  =   0 + (0.299    * r[i,j]) + (0.587    * g[i,j]) + (0.114    * b[i,j])
            cb[i,j] = 128 - (0.168736 * r[i,j]) + (0.331264 * g[i,j]) + (0.5      * b[i,j])
            cr[i,j] = 128 + (0.5      * r[i,j]) + (0.418688 * g[i,j]) + (0.081312 * b[i,j])
            
    return (y, cb, cr)

def ycbcr_to_rgb(Y, Cb, Cr):
    h, w = y.shape

    r = np.zeros((h,w))
    g = np.zeros((h,w))
    b = np.zeros((h,w))

    for i in range(h):
        for j in range(w):
            r[i,j] = y[i,j] + 1.402    * (cr[i,j] - 128)
            g[i,j] = y[i,j] - 0.344136 * (cb[i,j] - 128) - 0.714136 * (cr[i,j] - 128)
            b[i,j] = y[i,j] + 1.772    * (cb[i,j] - 128)

    return r,g,b

