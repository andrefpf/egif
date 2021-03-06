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

def correct_image_dimentions(matrix, levels=1):
    h, w = matrix.shape 
    h -= h % (1 << levels)
    w -= w % (1 << levels)
    result = matrix[:h, :w].copy()     
    return result

def create_chunks(matrices, chunk_size=4, levels=1):
    f = len(matrices)
    f -= f % chunk_size
    
    chunks = []
    matrices = matrices[:f]  # discard exedent frames 
    matrices = [correct_image_dimentions(matrix, levels) for matrix in matrices]

    for i in range(f // chunk_size):
        chunk = np.stack([matrices[i+j] for j in range(chunk_size)], axis=0)
        chunks.append(chunk)

    return chunks

def merge_matrices(a, b):
    h, w = a.shape
    merged = np.zeros((h,w))
    merged[0:h:2, :] = a[0:h:2, :]
    merged[1:h:2, :] = b[1:h:2, :]
    return merged

def rgb_to_ycbcr(r, g, b):
    h, w = r.shape

    y  =   0 + (0.299    * r) + (0.587    * g) + (0.114    * b)
    cb = 128 - (0.168736 * r) - (0.331264 * g) + (0.5      * b)
    cr = 128 + (0.5      * r) - (0.418688 * g) - (0.081312 * b)
            
    return (y.astype(int), cb.astype(int), cr.astype(int))

def ycbcr_to_rgb(y, cb, cr):
    h, w = y.shape

    r = y + 1.402    * (cr - 128) + 2
    g = y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128)
    b = y + 1.772    * (cb - 128) + 2

    return r.astype(int), g.astype(int), b.astype(int)

