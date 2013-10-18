
import pygame
from geometry import *

class Shape:
    def __init__(self):
        self.lines = []
        self.grabbed_point = None
        self.bounds = pygame.Rect(0,0,0,0)

    def getLines(self):
        lines = []
        for line in self.lines:
            lines.append(line.copy())
        return lines

    def newLine(self, p1, p2):
        self.lines.append(Line(p1.copy(), p2.copy()))
        self._updateBounds()

    def removeLine(self, point):
        # Remove the line containing the given point
        l = None
        for line in self.lines:
            if line.point1 == point or line.point2 == point:
                l = line
                break
        if l:
            self.lines.remove(l)
            self._updateBounds()

    def getPoint(self, pos):
        # Get the point within range of the given point
        if self.grabbed_point: # grabbed point has priority
            return self.grabbed_point
        for line in self.lines:
            if pos.inRange(line.point1):
                return line.point1.copy()
            elif pos.inRange(line.point2):
                return line.point2.copy()
        return None

    def grabPoint(self, point):
        for line in self.lines:
            if point == line.point1:
                point = line.point1
                break
            elif point == line.point2:
                point = line.point2
                break
        self.grabbed_point = point

    def releasePoint(self):
        self.grabbed_point = None

    def updatePoint(self, pos):
        # Moves the grabbed point to the given position
        if not self.grabbed_point: return False
        self.grabbed_point.x = pos.x
        self.grabbed_point.y = pos.y
        self._updateBounds()
        return True

    def _updateBounds(self):
        max_x = None
        max_y = None           
        for line in self.lines:
            if max_x:
                max_x = max(max_x, abs(line.point1.x), abs(line.point2.x))
            else:
                max_x = max(abs(line.point1.x), abs(line.point2.x))
            if max_y:
                max_y = max(max_y, abs(line.point1.y), abs(line.point2.y))
            else:
                max_y = max(abs(line.point1.y), abs(line.point2.y))

        max_x = max(10, max_x)
        max_y = max(10, max_y)
        self.bounds.topleft = (-max_x, -max_y)
        self.bounds.size = (2 * max_x, 2 * max_y)
