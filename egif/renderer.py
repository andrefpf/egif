import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets, QtGui
from time import time

from .files import read, write


class EgifViewer(QtWidgets.QGraphicsView):
    def __init__(self, parent, img=None):
        super(EgifViewer, self).__init__(parent)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.photo = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.photo)
        self.setScene(self.scene)
        self.setMinimumSize(256,256)

        self.timer = None
        self.current = None
        self.zoom = 0
        self.counter = 0
        self.pixmaps = []

        self.visualization()
        self.setImage(img)
    
    def visualization(self):
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        vertical = self.verticalScrollBar()
        horizontal = self.horizontalScrollBar()

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(10, 30, 30)))
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def createTimer(self):
        self.counter = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.loop)
        self.timer.start()

    def setImage(self, image=None):
        self.zoom = 100
        self.current = image

        if image is None:
            self.pixmaps = [QtGui.QPixmap()]   
        else:
            self.pixmaps = image.as_qpixmaps()

        self.render(self.pixmaps[0])
        self.play()
    
    def render(self, pixmap):
        self.photo.setPixmap(pixmap)

    def loop(self):
        if not self.pixmaps:
            return 
        self.counter = (self.counter + 1) % len(self.pixmaps)
        self.render(self.pixmaps[self.counter])

    def play(self):
        self.counter = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.loop)
        self.timer.start()

    def pause(self):
        if self.timer is not None:
            self.timer.stop()
    
    def zoomIn(self, factor=1.1):
        self.scale(factor, factor)

    def zoomOut(self, factor=1.1):
        img_size = self.photo.pixmap().rect()
        trs_size = self.transform().mapRect(img_size)
        too_small = (trs_size.width() <= 64) or (trs_size.height() <= 64)

        if not too_small:
            self.scale(1/factor, 1/factor)
    
    def setSpeed(self, speed):
        if self.timer is not None:
            self.timer.setInterval(speed)

    def wheelEvent(self, event):
        if self.current is None:
            return 
        
        delta = event.angleDelta().y()

        if delta > 0:
            self.zoomIn()
        elif delta < 0:
            self.zoomOut()

    def fitInView(self):
        if self.current is None:
            return 
        self.zoom = 100
        super().fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag) 
        super().mouseReleaseEvent(event)



class EgifWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, path=None):
        super().__init__(parent)

        self.viewer = EgifViewer(self)
        self.setCentralWidget(self.viewer)

        self.images_dir = []
        self.current_img = 0

        self.createIcons()
        self.createActions()
        self.configureWindow()
        self.createToolBar()

        if path is not None:
            self.read(path)
    
    def createIcons(self):
        self.egif_icon = QtGui.QIcon('icons/dummy.ico')
        self.last_image_icon = QtGui.QIcon.fromTheme('go-previous')
        self.next_image_icon = QtGui.QIcon.fromTheme('go-next')
        self.zoom_in_icon = QtGui.QIcon.fromTheme('zoom-in')
        self.zoom_out_icon = QtGui.QIcon.fromTheme('zoom-out')
        self.fit_icon = QtGui.QIcon.fromTheme('view-fullscreen')
        self.play_icon = QtGui.QIcon.fromTheme('media-playback-start')
        self.pause_icon = QtGui.QIcon.fromTheme('media-playback-pause')

    def createActions(self):
        self.last_image_action = QtWidgets.QAction(self.last_image_icon, 'last image', self)
        self.last_image_action.triggered.connect(self.lastImage)

        self.next_image_action = QtWidgets.QAction(self.next_image_icon, 'next image', self)
        self.next_image_action.triggered.connect(self.nextImage)

        self.zoom_in_action = QtWidgets.QAction(self.zoom_in_icon, 'zoom in', self)
        self.zoom_in_action.triggered.connect(self.zoomIn)

        self.zoom_out_action = QtWidgets.QAction(self.zoom_out_icon, 'zoom out', self)
        self.zoom_out_action.triggered.connect(self.zoomOut)

        self.fit_action = QtWidgets.QAction(self.fit_icon, 'fit image', self)
        self.fit_action.triggered.connect(self.fitInView)

        self.play_action = QtWidgets.QAction(self.play_icon, 'start animation', self)
        self.play_action.triggered.connect(self.play)

        self.pause_action = QtWidgets.QAction(self.pause_icon, 'pause animation', self)
        self.pause_action.triggered.connect(self.pause)

    def configureWindow(self):
        self.setWindowTitle('Egif Viewer')
        self.setWindowIcon(self.egif_icon)

    def createToolBar(self):       
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.last_image_action)
        self.toolbar.addAction(self.next_image_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.addAction(self.fit_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(self.pause_action)

    def showImage(self, image):
        self.viewer.setImage(image)

    def showImageFile(self, path):
        print(path)
        img = read(path)
        self.showImage(img)

    def read(self, path=''):
        path = Path(path)

        if not path.exists():
            print("This path doesn't exists.")
            return

        file = None
        if path.is_file():
            file = path 
            path = path.parent
        
        self.images_dir = [i.as_posix() for i in path.glob('*.egif')]

        if file is None:
            self.dir_counter = 0
        else:
            self.dir_counter = self.images_dir.index(file.as_posix())

        current_path = self.images_dir[self.dir_counter]
        self.showImageFile(current_path)

    def nextImage(self):
        if len(self.images_dir) <= 1:
            return 
        self.dir_counter = (self.dir_counter + 1) % len(self.images_dir)
        path = self.images_dir[self.dir_counter]
        self.showImageFile(path)

    def lastImage(self):
        if len(self.images_dir) <= 1:
            return 
        self.dir_counter = (self.dir_counter - 1) % len(self.images_dir)
        path = self.images_dir[self.dir_counter]
        self.showImageFile(path)

    def zoomIn(self):
        self.viewer.zoomIn(1.5)

    def zoomOut(self):
        self.viewer.zoomOut(1.5)
    
    def fitInView(self):
        self.viewer.fitInView()

    def play(self):
        self.viewer.play()
        
    def pause(self):
        self.viewer.pause()



def run_app(path=None):
    app = QtWidgets.QApplication(sys.argv)
    window = EgifWindow(path=path)
    window.show()
    app.exec_()



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
