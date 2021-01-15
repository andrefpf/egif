import numpy as np
from PyQt5.QtGui import QPixmap, QImage


class EgifImage:
    def __init__(self, matrix):
        self.width = None 
        self.height = None
        self.frames = None 

        self.r = None 
        self.g = None 
        self.b = None 

        self.load_matrix(matrix)

    def as_rgb(self):
        matrix = np.stack((self.r, self.g, self.b), axis=3)
        matrix = np.clip(matrix, 0, 255).astype(np.uint8)
        return matrix
    
    def as_qimages(self):
        fmt = QImage.Format_RGB888
        qimage = lambda x: QImage(x.data, self.width, 
                                  self.height, self.width*3, fmt)
        return [qimage(i) for i in self.as_rgb()]

    def as_qpixmaps(self):
        return [QPixmap(i) for i in self.as_qimages()]

    def load_matrix(self, matrix):
        if matrix.ndim == 3:
            self._load_bw(matrix)
        elif (matrix.ndim == 4) and (matrix.shape[3] >= 3):
            self._load_rgb(matrix)
        else:
            raise ValueError('Deu merda')

    def _load_bw(self, matrix):
        if matrix.ndim != 3:
            raise ValueError('Image should be 3 dimentional.')

        bw = self._trim(matrix)
        self.frames, self.height, self.width = bw.shape
        self.r = bw

    def _load_rgb(self, matrix):
        if (matrix.ndim != 4) or (matrix.shape[3] < 3):
            raise ValueError('Image should be 3 dimentional.')

        r = matrix[:,:,:,0]
        g = matrix[:,:,:,1]
        b = matrix[:,:,:,2]

        r = self._trim(r)
        g = self._trim(g)
        b = self._trim(b)

        self.frames, self.height, self.width = r.shape

        self.r = r
        self.g = g
        self.b = b

    def _trim(self, matrix, block_size=8):
        f, h, w = matrix.shape

        if (h < block_size) or (w < block_size):
            raise ValueError('This matrix is very small.')

        nf = f - f % block_size
        nh = h - h % block_size
        nw = w - w % block_size

        new_matrix = np.zeros((nf, nh, nw), dtype=int)
        new_matrix[:f, :, :] = matrix[:, :nh, :nw] 
        
        for i in range(f, nf):
            new_matrix[i] = matrix[-1, :nh, :nw]
        
        return new_matrix

    def __eq__(self, other):
        return self.to_rgb == other.to_rgb