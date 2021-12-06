import sys
from mazeview import MazeView

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    XSIZEDEFAULT = 10
    YSIZEDEFAULT = 10
    def __init__(self):
        super(MainWindow, self).__init__()

        # MENU BAR
        # ----------------------------------------------------------------------
        game = self.menuBar().addMenu("Maze")
        load = QAction("Change size", self)
        load.triggered.connect(self.openSettingsWindow)
        game.addAction(load)

        # MAZE VIEW WIDGET
        # ----------------------------------------------------------------------
        self.rows = self.YSIZEDEFAULT
        self.columns = self.XSIZEDEFAULT
        self.maze = MazeView(parent=self)
        self.maze.newMaze(self.rows, self.columns)

        # MAZE GENERATION CONTROL WIDGET
        # ----------------------------------------------------------------------
        self.regenerateButton = QPushButton("Regenerate", parent=self)
        self.regenerateButton.clicked.connect(self.regenerateMaze)

        # LAYOUTS
        # ----------------------------------------------------------------------
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.maze)
        vlayout.addWidget(self.regenerateButton)

        # CENTRAL WIDGET
        # ----------------------------------------------------------------------
        cwidget = QWidget(parent=self)
        cwidget.setLayout(vlayout)
        self.setCentralWidget(cwidget)

    def openSettingsWindow(self):
        self.swindow = SettingsWindow(self.rows, self.columns, parent=self)
        self.swindow.send.connect(self._changeSize)
        self.swindow.show()

    @Slot(int, int)
    def _changeSize(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.regenerateMaze()
        self.maze.fitInView(self.maze.scene.sceneRect(), Qt.KeepAspectRatio)

    def regenerateMaze(self):
        self.maze.newMaze(self.rows, self.columns)

class SettingsWindow(QDialog):
    send = Signal(int,int)
    def __init__(self, rows, columns, parent=None):
        super(SettingsWindow, self).__init__(parent=parent)
        self.setWindowTitle("Maze size")

        # Top widget
        twidget = QWidget(parent=self)

        label1 = QLabel("Rows:", parent=self)
        label2 = QLabel("Columns:", parent=self)
        label1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.spbox1 = QSpinBox(parent=self)
        self.spbox1.setRange(3,150)
        self.spbox1.setValue(rows)
        self.spbox2 = QSpinBox(parent=self)
        self.spbox2.setRange(3,150)
        self.spbox2.setValue(columns)

        glayout = QGridLayout()
        glayout.addWidget(label1, 0, 0)
        glayout.addWidget(label2, 1, 0)
        glayout.addWidget(self.spbox1, 0, 1)
        glayout.addWidget(self.spbox2, 1, 1)

        twidget.setLayout(glayout)

        # Bottom widget
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # Full widget
        flayout = QVBoxLayout()
        flayout.addWidget(twidget)
        flayout.addWidget(buttonBox)

        self.setLayout(flayout)

    def accept(self):
        self.send.emit(self.spbox1.value(), self.spbox2.value())
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

