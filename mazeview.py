import sys
from maze import Maze

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

class MazeView(QGraphicsView):
    side = 20
    margin = 20
    wallwidth = 3

    def __init__(self, parent=None):
        super(MazeView, self).__init__(parent=parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)

    def newMaze(self, rows, columns):
        self.rows = rows
        self.columns = columns

        width = self.margin * 2 + self.side * columns
        height = self.margin * 2 + self.side * rows

        self.scene = QGraphicsScene(parent=self)
        self.scene.setSceneRect(0, 0, width, height)
        self.scene.setBackgroundBrush(QBrush(QColor(255,255,255,255)))

        self.maze = Maze(rows, columns)
        self._paintMaze()

        self.setScene(self.scene)

    def _paintMaze(self):
        pen = QPen()
        pen.setWidth(self.wallwidth)
        for i in range(self.rows+1):
            for j in range(self.columns+1):
                # Horizontal wall
                if j < self.columns:
                    connected = False
                    if i > 0 and self.maze.maze[i-1][j] == (i,j):
                        connected = True
                    elif i < self.rows and self.maze.maze[i][j] == (i-1,j):
                        connected = True
                    elif self.maze.exit in ((i,j), (i-1,j)):
                        connected = True

                    if not connected:
                        x1 = self.margin + self.side * j
                        y1 = self.margin + self.side * i
                        x2 = self.margin + self.side * (j+1)
                        y2 = y1
                        self.scene.addLine(x1,y1,x2,y2,pen=pen)

                # Vertical wall
                if i < self.rows:
                    connected = False
                    if j > 0 and self.maze.maze[i][j-1] == (i,j):
                        connected = True
                    elif j < self.columns and self.maze.maze[i][j] == (i,j-1):
                        connected = True
                    elif self.maze.exit in ((i,j), (i,j-1)):
                        connected = True

                    if not connected:
                        x1 = self.margin + self.side * j
                        y1 = self.margin + self.side * i
                        x2 = x1
                        y2 = self.margin + self.side * (i+1)
                        self.scene.addLine(x1,y1,x2,y2,pen=pen)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

if __name__ == "__main__":
    app = QApplication([])

    window = MazeView()
    window.newMaze(50,50)
    window.show()

    sys.exit(app.exec_())
