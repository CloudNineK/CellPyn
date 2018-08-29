import sys
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp,
                             QHBoxLayout, QVBoxLayout, QLabel, QApplication,
                             QWidget, QTabWidget, QFileDialog)


class View(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.title = 'CellPyn'
        self.fname = ''

    def initUI(self):

        self.statusBar()
        menubar = self.menuBar()

        # ACTIONS
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
        plusAct = QAction('Add Module', self)
        plusAct.setStatusTip('Add new module')
        plusAct.triggered.connect(self.addModule)

        # MENUBAR
        # File
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(openAct)

        # Edit
        fileMenu = menubar.addMenu('&Edit')
        # Possibly add undo / redo here

        # Help
        fileMenu = menubar.addMenu('&Help')

        # Layout
        layout = Layout()
        self.setCentralWidget(layout)

        # Toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        self.move(300, 200)
        self.show()

    def fileDialog(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open File', '/home')
        print(self.fname[0])

    def addModule(self):
        pass


class Layout(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.layout = QHBoxLayout(self)

        pipe = Pipeline()
        self.layout.addWidget(pipe)

        rPanel = RightPanel()
        self.layout.addWidget(rPanel)


class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)


class Pipeline(QWidget):

    def __init__(self):
        super().__init__()

        # Setup Tabs
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        # self.tabs.resize(300, 200)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.testTab()

    def testTab(self):
        lbl = QLabel()
        pixmap = QPixmap("OnionEpidermis.jpg")
        lbl.setPixmap(pixmap)

        tab = QWidget()
        tab.resize(300, 300)
        tab.layout = QVBoxLayout(self)
        tab.layout.addWidget(lbl)

        tab.setLayout(tab.layout)

        self.tabs.addTab(tab, "Test")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    view = View()

    sys.exit(app.exec_())
