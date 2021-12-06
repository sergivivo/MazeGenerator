import sys
import random

class Maze:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.maze = [[None for _ in range(columns)] for _ in range(rows)]
        self._generateMaze()

    def _generateMaze(self):
        borders = [(i,j) for i in (0, self.rows    - 1) for j in range(1, self.columns - 1)] + \
                  [(i,j) for j in (0, self.columns - 1) for i in range(1, self.rows    - 1)] + \
                  [(0, 0), (0, self.columns-1), (self.rows-1, 0), (self.rows-1, self.columns-1)]

        # Root of the maze
        self.root = random.choice(borders)
        i, j = self.root
        adjacent = self._getNeighborOOB(i,j)
        innerwalls = self._getNeighbor(i,j)
        outerwalls = [w for w in adjacent if w not in innerwalls]
        self.maze[i][j] = random.choice(outerwalls)

        # Exit
        borders.remove(self.root)
        lastcell = random.choice(borders)
        i, j = lastcell
        adjacent = self._getNeighborOOB(i,j)
        innerwalls = self._getNeighbor(i,j)
        outerwalls = [w for w in adjacent if w not in innerwalls]
        self.exit = random.choice(outerwalls)

        # Generating the maze
        self._depthSearch()

    def _depthSearch(self):
        visited = [self.root]
        stack = [self.root]
        while len(stack) > 0:
            visiting = stack.pop()
            i, j = visiting
            neighbor = self._getNeighbor(i, j)
            unvisited = [e for e in neighbor if e not in visited]
            if len(unvisited) > 0:
                stack.append(visiting)
                chosen = random.choice(unvisited)
                i, j = chosen
                self.maze[i][j] = visiting
                visited.append(chosen)
                stack.append(chosen)

    def _getNeighborOOB(self, row, column):
        return [(i,j) for i in range(row    - 1, row    + 2)
                      for j in range(column - 1, column + 2)
                      if (i+j) % 2 != (row+column) % 2]

    def _getNeighbor(self, row, column):
        return [(i,j) for i in range(max(0, row    - 1), min(row    + 2, self.rows   ))
                      for j in range(max(0, column - 1), min(column + 2, self.columns))
                      if (i+j) % 2 != (row+column) % 2]


    def __repr__(self):
        s = ""
        for i in range(self.rows*2+1):
            for j in range(self.columns*2+1):
                if i % 2 == 0 and j % 2 == 0:
                    # Wall intersection
                    s += "+"
                elif i % 2 == 0:
                    # Horizontal wall
                    x  = int((j - 1) / 2)
                    y1 = int(i / 2 - 1)
                    y2 = int(i / 2)
                    if y1 >= 0 and self.maze[y1][x] == (y2,x):
                        s += "   "
                    elif y2 < self.rows and self.maze[y2][x] == (y1,x):
                        s += "   "
                    elif self.exit in ((x,y1), (x,y2)):
                        s += "   "
                    else:
                        s += "---"
                elif j % 2 == 0:
                    # Vertical wall
                    x1 = int(j / 2 - 1)
                    x2 = int(j / 2)
                    y  = int((i - 1) / 2)
                    if x1 >= 0 and self.maze[y][x1] == (y,x2):
                        s += " "
                    elif x2 < self.columns and self.maze[y][x2] == (y,x1):
                        s += " "
                    elif self.exit in ((x1,y), (x2,y)):
                        s += " "
                    else:
                        s += "|"
                else:
                    # Cell
                    s += "   "
            s += "\n"
        return s



if __name__ == "__main__":
    rows    = 10   if len(sys.argv) < 2 else int(sys.argv[1])
    columns = rows if len(sys.argv) < 3 else int(sys.argv[2])
    maze = Maze(rows,columns)
    print(maze)
