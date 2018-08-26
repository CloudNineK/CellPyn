import sys
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp,
                             QHBoxLayout, QVBoxLayout, QLabel, QApplication,
                             QWidget, QTabWidget)


class View(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.title = 'CellPyn'

    def initUI(self):

        self.statusBar()
        menubar = self.menuBar()

        # ACTIONS
        # Exit Action
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        # MENUBAR
        # File
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        # Edit
        fileMenu = menubar.addMenu('&Edit')

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


class Layout(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.layout = QHBoxLayout(self)

        tabs = Tabs()
        self.layout.addWidget(tabs)

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

        # Initialize tabs
        self.tabs = QTabWidget()
        self.firstTab = QWidget()
        self.secondTab = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.firstTab, "Default")
        self.tabs.addTab(self.secondTab, "Two")
        self.testTab()

    def testTab(self):
        pixmap = QPixmap("OnionEpidermis.jpg")

        lbl = QLabel()
        lbl.setPixmap(pixmap)

        self.firstTab.layout = QHBoxLayout(self)
        self.firstTab.layout.addWidget(lbl)

        self.tabs.addTab(self.firstTab, "Default")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    view = View()

    sys.exit(app.exec_())
