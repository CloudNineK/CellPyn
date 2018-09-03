import sys
import os
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp,
                             QHBoxLayout, QVBoxLayout, QLabel, QApplication,
                             QWidget, QTabWidget, QFileDialog, QListWidget)

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
        self.fname = QFileDialog.getOpenFileName(self, 'Open File',
                                                 os.getcwd())
        self.centralWidget().pipe.firstTab(self.fname[0])
        print(self.fname[0])

    def moduleDialog(self):
        """ Dialog connected to the Open Action.
        """
        pass


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

        # Setup Tabs
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        # self.tabs.resize(300, 200)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.pipe = []
        # Modules
        self.modules = {}
        self.modules['Threshold'] = Threshold()

    def firstTab(self, fname):
        lbl = QLabel()
        pixmap = QPixmap(fname)
        lbl.setPixmap(pixmap)

        tab = QWidget()
        tab.resize(300, 300)
        tab.layout = QVBoxLayout(self)
        tab.layout.addWidget(lbl)

        tab.setLayout(tab.layout)

        self.tabs.addTab(tab, "Test")
        pass

    def addModule():
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    view = View()

    sys.exit(app.exec_())
