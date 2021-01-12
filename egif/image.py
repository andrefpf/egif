import numpy as np
from PIL import Image

class EgifImage:
    def __init__(self, matrix, mode='ycbcr'):
        self.width = None 
        self.height = None
        self.frames = None 

        self.y = None 
        self.cb = None 
        self.cr = None 
        
        if mode == 'ycbcr':
            self.load_from_ycbcr(matrix)
        else:
            raise ValueError('Deu merda, amigo.')

    def load_from_ycbcr(self, ycbcr):
        y, cb, cr = ycbcr

        if not (y.shape == cb.shape == cr.shape):
            raise ValueError('Image shapes are not right.')
        
        if y.ndim == 2:
            self.frames = 1
            self.height = y.shape[0]
            self.width = y.shape[1]
        elif y.ndim == 3:
            self.frames = y.shape[0]
            self.height = y.shape[1]
            self.width = y.shape[2]
        else:
            raise ValueError('Image should be 2 or 3 dimentional.')

        self.y = y
        self.cb = cb
        self.cr = cr

def load_images(paths, shape=(256,256)):
    y = []
    cb = []
    cr = []

    for path in paths:
        img = Image.open(path)
        img = img.resize(shape)
        # img = img.convert('YCbCr')

        matrix = np.asarray(img, dtype=int)

        y.append(matrix[:,:,0])
        cb.append(matrix[:,:,1])
        cr.append(matrix[:,:,2])

    y = np.stack(y)
    cb = np.stack(cb)
    cr = np.stack(cr)

    return EgifImage((y,cb,cr))

def load_image(path, shape=(256,256)):
    img = Image.open(path)
    img = img.resize(shape)
    # img = img.convert('YCbCr')

    matrix = np.asarray(img, dtype=int)
    y = matrix[:,:,0]
    cb = matrix[:,:,1]
    cr = matrix[:,:,2]

    return EgifImage((y,cb,cr), mode='ycbcr')

def write_image(animage):
    pass

