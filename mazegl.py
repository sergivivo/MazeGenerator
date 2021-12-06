import sys
import math

from PySide2.QtGui     import *
from PySide2.QtCore    import *
from PySide2.QtOpenGL  import *
from PySide2.QtWidgets import *

from OpenGL.GL  import *
from OpenGL.GLU import *

from maze import Maze

class MazeGL(QOpenGLWidget):
    initialFOV = 60.0
    FPS = 60
    def __init__(self, parent=None):
        super(MazeGL, self).__init__(parent=parent)

        # Camera parameters
        self.xRot = 0.0
        self.yRot = 0.0
        self.xPos = 0.0
        self.zPos = 0.0
        self.fov = self.initialFOV

        # Keyboard movement
        self.keys = 0
        self.floating = False
        self.moving = False
        self.timer = QTimer(parent=self)
        self.connect(self.timer, SIGNAL('timeout()'), self._updatePosition)

        # Center of the widget
        self.center = QPoint(self.width()/2, self.height()/2)

    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(self.fov, self.width()/self.height(), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClearColor(0.5, 0.7, 1.0, 1.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        self.walltexture = QOpenGLTexture(QImage('bricks.jpg').mirrored())
        self.floortexture = QOpenGLTexture(QImage('floor.jpg').mirrored())

        self.newMaze(20,20)

    def newMaze(self, rows, columns):
        self.rows = rows
        self.columns = columns

        self.maze = Maze(rows, columns)
        self.mazeObject = self._makeMaze()
        self.floorObject = self._makeFloor()
        self.repaint()

    def _makeMaze(self):

        genList = glGenLists(1)
        glNewList(genList, GL_COMPILE)

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
                        x1 = 2.0 + 2.0 * j
                        y1 = 2.0 + 2.0 * i
                        x2 = 2.0 + 2.0 * (j+1)
                        y2 = y1

                        glBegin(GL_QUADS)

                        glTexCoord2f(0.0,  0.0)
                        glVertex3f(  x1, -1.0,  y1)
                        glTexCoord2f(1.0,  0.0)
                        glVertex3f(  x2, -1.0,  y2)
                        glTexCoord2f(1.0,  1.0)
                        glVertex3f(  x2,  1.0,  y2)
                        glTexCoord2f(0.0,  1.0)
                        glVertex3f(  x1,  1.0,  y1)

                        glEnd()

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
                        x1 = 2.0 + 2.0 * j
                        y1 = 2.0 + 2.0 * i
                        x2 = x1
                        y2 = 2.0 + 2.0 * (i+1)

                        glBegin(GL_QUADS)

                        glTexCoord2f(0.0,  0.0)
                        glVertex3f(  x1, -1.0,  y1)
                        glTexCoord2f(1.0,  0.0)
                        glVertex3f(  x2, -1.0,  y2)
                        glTexCoord2f(1.0,  1.0)
                        glVertex3f(  x2,  1.0,  y2)
                        glTexCoord2f(0.0,  1.0)
                        glVertex3f(  x1,  1.0,  y1)

                        glEnd()

        glEndList()
        return genList

    def _makeFloor(self):
        genList = glGenLists(1)
        glNewList(genList, GL_COMPILE)

        glBegin(GL_QUADS)

        glTexCoord2f(0.0,  0.0)
        glVertex3f(  2.0, -1.0, 2.0)
        glTexCoord2f(1.0,  0.0)
        glVertex3f(  2.0, -1.0, 2.0 + 2*self.rows)
        glTexCoord2f(1.0,  1.0)
        glVertex3f(  2.0 + 2*self.columns, -1.0,  2.0 + 2*self.rows)
        glTexCoord2f(0.0,  1.0)
        glVertex3f(  2.0 + 2*self.columns, -1.0,  2.0)

        glEnd()

        glEndList()
        return genList

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glRotatef(-self.xRot, 1.0, 0.0, 0.0)
        glRotatef(-self.yRot, 0.0, 1.0, 0.0)

        if self.floating:
            glTranslate(0.0, -10.0, 0.0)
        glTranslate(-self.xPos, 0.0, -self.zPos)

        self.walltexture.bind()
        glCallList(self.mazeObject)
        self.walltexture.release()

        self.floortexture.bind()
        glCallList(self.floorObject)
        self.floortexture.release()

        glPopMatrix()

    def resizeGL(self, width, height):
        # Redefine the center of the widget
        self.center = QPoint(self.width()/2, self.height()/2)

        # Change viewport and camera
        side = min(width, height)
        glViewport(int((width - side) / 2), int((height - side) / 2), side, side)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))
        QCursor.setPos(self.mapToGlobal(self.center))
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.hasMouseTracking() and event.pos() != self.center:
            # Increments respect to the center
            xinc = self.center.x() - event.x()
            yinc = self.center.y() - event.y()

            # Add the increment to the angle, formating
            self.xRot += yinc * 360 / 3000
            self.xRot = min(self.xRot, 90) if self.xRot > 0 else max(self.xRot, -90)
            self.yRot += xinc * 360 / 3000
            self.yRot %= 360

            # Return cursor to the center
            QCursor.setPos(self.mapToGlobal(self.center))

            self.repaint()

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            # Remove mouse tracking
            if event.key() == Qt.Key_Escape:
                QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
                self.setMouseTracking(False)

            # Each key represents a bit
            if   event.key() == Qt.Key_W:
                self.keys |= 1
            elif event.key() == Qt.Key_A:
                self.keys |= 2
            elif event.key() == Qt.Key_S:
                self.keys |= 4
            elif event.key() == Qt.Key_D:
                self.keys |= 8
            elif event.key() == Qt.Key_Space:
                self.floating = not self.floating

            if self.keys != 0 and not self.moving:
                self._startMoving()

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            # Two's complement negative numbers acting as an inverse mask
            if   event.key() == Qt.Key_W:
                self.keys &= -2
            elif event.key() == Qt.Key_A:
                self.keys &= -3
            elif event.key() == Qt.Key_S:
                self.keys &= -5
            elif event.key() == Qt.Key_D:
                self.keys &= -9

            if self.keys == 0:
                self._stopMoving()

    def _startMoving(self):
        self.moving = True
        self.timer.start(1000/self.FPS)

    def _stopMoving(self):
        self.moving = False
        self.timer.stop()

    def _updatePosition(self):
        xInc = math.sin(math.radians(self.yRot)) * 3/self.FPS
        zInc = math.cos(math.radians(self.yRot)) * 3/self.FPS
        if self.keys & 1 != 0:
            self.xPos -= xInc
            self.zPos -= zInc
        if self.keys & 2 != 0:
            self.xPos -= zInc
            self.zPos += xInc
        if self.keys & 4 != 0:
            self.xPos += xInc
            self.zPos += zInc
        if self.keys & 8 != 0:
            self.xPos += zInc
            self.zPos -= xInc
        self.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MazeGL()
    window.show()
    sys.exit(app.exec_())
