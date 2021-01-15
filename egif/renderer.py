import matplotlib.pyplot as plt

import sys
import numpy as np
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
# from PyQt5.QtGui import QPixmap, QImage, QPalette
from PyQt5 import QtCore, QtWidgets, QtGui


class EgifViewer(QtWidgets.QGraphicsView):
    def __init__(self, parent, img=None):
        super(EgifViewer, self).__init__(parent)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.photo = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.photo)
        self.setScene(self.scene)
        self.setMinimumSize(256,256)

        self.zoom = 0
        self.pixmaps = []

        self.createTimer()
        self.visualization()
        self.setImage(img)
    
    def visualization(self):
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        vertical = self.verticalScrollBar()
        horizontal = self.horizontalScrollBar()

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(20, 0, 20)))
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def createTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.loop)
        self.counter = 0

    def setImage(self, image):
        if image is None:
            return

        self.zoom = 100
        self.current = image
        self.pixmaps = image.as_qpixmaps()

        self.render(self.pixmaps[0])
        self.timer.start()
    
    def render(self, pixmap):
        self.photo.setPixmap(pixmap)

    def loop(self):
        if not self.pixmaps:
            return 
        self.counter = (self.counter + 1) % len(self.pixmaps)
        self.render(self.pixmaps[self.counter])

    def wheelEvent(self, event):
        factor = 1.1
        delta = event.angleDelta().y()

        img_size = self.photo.pixmap().rect()
        trs_size = self.transform().mapRect(img_size)
        min_size = (64, 64)

        in_x = trs_size.width() > min_size[0]
        in_y = trs_size.height() > min_size[1]

        if delta > 0:
            self.scale(factor, factor)
        elif delta < 0 and in_x and in_y:
            self.scale(1/factor, 1/factor)

        self.zoom = trs_size.width() * 100 // img_size.width() 
    
    def fitInView(self):
        self.zoom = 100
        super().fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag) 
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_R:
            self.fitInView()



class EgifWindow(QtWidgets.QMainWindow):
    def __init__(self, img, parent=None):
        super().__init__(parent)

        # self.resize(400, 400)

        self.viewer = EgifViewer(self)
        self.setCentralWidget(self.viewer)

    def mostrar(self, image):
        self.viewer.setImage(image)


def show_image(matrix):
    plt.imshow(matrix, vmin=0, vmax=255, cmap='gray')
    plt.show()

def compare_images(matrix_a, matrix_b):
    fig = plt.figure()

    ax = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(matrix_a, vmin=0, vmax=255, cmap='gray')

    ax = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(matrix_b, vmin=0, vmax=255, cmap='gray')

    plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = EgifWindow()
    window.show()

    app.exec_()