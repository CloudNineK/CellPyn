import sys
import os
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp,
                             QHBoxLayout, QVBoxLayout, QLabel, QApplication,
                             QWidget, QTabWidget, QFileDialog, QInputDialog,
                             QListWidget)

from cv2 import imread
from PynModules import Threshold


class View(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.title = 'CellPyn'
        self.fname = ''
        self.resize(400, 300)

    def initUI(self):

        self.statusBar()
        menubar = self.menuBar()

        # --- ACTIONS ------------------------------------------------------->
        # Exit Action
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        # Open Action
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open Image')
        openAct.triggered.connect(self.fileDialog)

        # Add Module Action
        plusAct = QAction(QIcon('plus.png'), 'Add Module', self)
        plusAct.setStatusTip('Add new module')
        plusAct.triggered.connect(self.moduleDialog)

        # --- MENUBAR ------------------------------------------------------->
        # File
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(openAct)

        # Edit
        fileMenu = menubar.addMenu('&Edit')
        # Possibly add undo / redo here

        # Help
        fileMenu = menubar.addMenu('&Help')

        # --- LAYOUT -------------------------------------------------------->
        layout = Layout()
        self.setCentralWidget(layout)

        # Toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(plusAct)

        self.move(300, 200)
        self.show()

    def fileDialog(self):
        """ Dialog connected to the Open Action.
            Starts in current working directory
        """
        f = QFileDialog.getOpenFileName(self, 'Open File', os.getcwd())
        self.fname = f[0]
        self.centralWidget().pipe.fname = self.fname
        self.centralWidget().pipe.firstTab()

    def moduleDialog(self):
        """ Dialog connected to the Open Action.
        """

        # TODO: Get this tuples from a list of modules
        modules = ("Threshold", "N/A1", "N/A2")

        module, okPressed = QInputDialog.getItem(self, "Select Module",
                                                 "Selection: ", modules, 0,
                                                 True)
        self.centralWidget().pipe.addModule(module)


class Layout(QWidget):

    def __init__(self):
        super().__init__()
        self.pipe = Pipeline()
        self.rPanel = RightPanel()

        self.initUI()

    def initUI(self):

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.pipe)

        self.layout.addWidget(self.rPanel)


class RightPanel(QWidget):
    """ Side panel used to adjust values for PynModule parameters"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)


class Pipeline(QWidget):
    """ Organizational class for managing PynModules added in sequence

        Top-level class manages tab widget display"""

    # TODO: Make sure pipeline facilitates insertion and movement

    def __init__(self):
        super().__init__()

        # Tabs / Layout
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Modules
        self.fname = None
        self.img = None
        self.imgMode = True
        self.pipe = []
        self.modules = {}
        self.modules['Threshold'] = Threshold()

    def firstTab(self):

        # Label
        lbl = QLabel()
        pixmap = QPixmap(self.fname)
        lbl.setPixmap(pixmap)

        # Tab Setup
        tab = QWidget()
        tab.resize(300, 300)
        tab.layout = QVBoxLayout(self)
        tab.layout.addWidget(lbl)

        tab.setLayout(tab.layout)

        self.tabs.addTab(tab, "Raw")

    def addModule(self, moduleName: str):

        # Module
        module = self.modules[moduleName]
        img = self.getImg()

        # hardcoded blur for init; remove when not testing
        proc = module.app(img, 3)

        # Label
        lbl = QLabel()
        pixmap = QPixmap(self.cvToPixmap(proc))
        lbl.setPixmap(pixmap)

        # Tab Setup
        tab = QWidget()
        tab.resize(300, 300)
        tab.layout = QVBoxLayout(self)
        tab.layout.addWidget(lbl)

        tab.setLayout(tab.layout)

        self.tabs.addTab(tab, moduleName)
        pass

    def getImg(self):
        if self.img is None and self.imgMode:
            self.img = imread(self.fname, 1)

        return self.img

    def cvToPixmap(self, img):
        """ Convert openCV image to QPixmap
            TODO: Port to PynModule
                  bytesPerLine = width * 1 is only for B/W images
        """
        print(img.shape)
        height, width = img.shape
        bytesPerLine = width
        qImg = QImage(img.data, width, height, bytesPerLine,
                      QImage.Format_Grayscale8)
        return qImg


if __name__ == '__main__':

    app = QApplication(sys.argv)
    view = View()

    sys.exit(app.exec_())
