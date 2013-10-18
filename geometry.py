
from math import sqrt, sin, cos, radians

class Coords:
    def __init__(self, pos, scale, angle):
        self.pos = pos
        self.scale = scale
        self.angle = angle

    def shiftCoords(self, coords):
        s = (self.scale[0] * coords.scale[0], self.scale[1] * coords.scale[1])
        a = (coords.angle + self.angle) % 360
        p = coords.applyCoords(self.pos)
        return Coords(p, s, a)

    def applyCoords(self, point):
        scaled = Point(point.x * self.scale[0], point.y * self.scale[1])
        rotated = Point.rotate(scaled, self.angle)
        translated = Point(rotated.x + self.pos.x, rotated.y + self.pos.y)
        return translated

    def __repr__(self):
        return "Coords: (%.2f, %.2f) [%.2f, %.2f] %.2f*" % (self.pos.x, self.pos.y, self.scale[0], self.scale[1], self.angle)

class Point:
    RANGE = 5
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def inRange(self, point):
        line = Line(self, point)
        return line.length() <= self.RANGE

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y

    def rotate(point, angle):
        c = cos(radians(angle))
        s = sin(radians(angle))
        
        new_point = Point()
        new_point.x = c * point.x + s * point.y
        new_point.y = -s * point.x + c * point.y
        return new_point

class Line:
    def __init__(self, p1, p2):
        self.point1 = p1
        self.point2 = p2

    def copy(self):
        return Line(self.point1.copy(), self.point2.copy())

    def length(self):
        return sqrt((self.point1.x - self.point2.x) ** 2 +
                    (self.point1.y - self.point2.y) ** 2)

    def __eq__(self, other):
        return (other and
                (self.point1 == other.point1 and
                 self.point2 == other.point2) or
                (self.point1 == other.point2 and
                 self.point2 == other.point1))

class BoxControl:
    # Modifies the properties of the box based on it's control points.
    def __init__(self, box):
        self.box = box

        half_width = self.box.width / 2
        half_height = self.box.height / 2
        left = self.box.center.x - half_width
        right = self.box.center.x + half_width
        top = self.box.center.y - half_height
        bottom = self.box.center.y + half_height
        
        self.topleft = Point(top, left)
        self.topright = Point(top, right)
        self.bottomleft = Point(bottom, left)
        self.bottomright = Point(bottom, right)

    #def getPoint
        
class Box:
    def __init__(self, position, size, angle=0):
        self.center = position
        self.width = size[0]
        self.height = size[1]
        self.angle = angle

    def getCorners(self):
        # return list of for corners' locations
        pass

    def pointWithin(self, point):
        pass
        # rotate point by -self.angle
        # return rect.left <= point.x <= rect.right and rect.bottom <= point.y <= rect.top
        
