
from shape import *
from geometry import Coords, Point
from math import cos, atan, sqrt, degrees

class ShapeStamp:
    TRANSLATE, SCALE_TL, SCALE_BR, ROTATE_TR, ROTATE_BL = range(5)
    def __init__(self, position=Point(), scale=(1.0, 1.0), angle=0):
        self.pos = position
        self.scale = scale
        self.angle = angle
        self.control_size = 10

    def coords(self):
        return Coords(self.pos, self.scale, self.angle)

    def copy(self):
        return ShapeStamp(self.pos, self.scale, self.angle)

    # Returns which portion of the stamp the point is within or None
    # if the point is not within the stamp.
    def pointWithin(self, point, size):
        point = point.copy()
        point.x -= self.pos.x
        point.y -= self.pos.y
        point = Point.rotate(point, -self.angle)
        # Must shift coordinates back
        point.x += self.pos.x
        point.y += self.pos.y
        half_width = size[0] * self.scale[0] / 2.0
        half_height = size[1] * self.scale[1] / 2.0
        # For mirrored position the control points are mirrored as well.
        hw = half_width
        hh = half_height
        half_width = abs(half_width)
        half_height = abs(half_height)
        left = self.pos.x - half_width
        right = self.pos.x + half_width
        top = self.pos.y - half_height
        bottom = self.pos.y + half_height
        if left <= point.x <= right and top <= point.y <= bottom:
            if left <= point.x <= left + self.control_size:
                if top <= point.y <= top + self.control_size:
                    if hw >= 0:
                        if hh >= 0:
                            return self.SCALE_TL
                        else:
                            return self.ROTATE_BL
                    else:
                        if hh >= 0:
                            return self.ROTATE_TR
                        else:
                            return self.SCALE_BR
                elif bottom - self.control_size <= point.y <= bottom:
                    if hw >= 0:
                        if hh >= 0:
                            return self.ROTATE_BL
                        else:
                            return self.SCALE_TL
                    else:
                        if hh >= 0:
                            return self.SCALE_BR
                        else:
                            return self.ROTATE_TR
            elif right - self.control_size <= point.x <= right:
                if top <= point.y <= top + self.control_size:
                    if hw >= 0:
                        if hh >= 0:
                            return self.ROTATE_TR
                        else:
                            return self.SCALE_BR
                    else:
                        if hh >= 0:
                            return self.SCALE_TL
                        else:
                            return self.ROTATE_BL
                elif bottom - self.control_size <= point.y <= bottom:
                    if hw >= 0:
                        if hh >= 0:
                            return self.SCALE_BR
                        else:
                            return self.ROTATE_TR
                    else:
                        if hh >= 0:
                            return self.ROTATE_BL
                        else:
                            return self.SCALE_TL
                # There is probably a better way to do that, but I'm not going to worry about it :)
            return self.TRANSLATE
        else:
            return None

    def __eq__(self, other):
        return other and (self.pos == other.pos and
                self.scale == other.scale and
                self.angle == other.angle)
        
class Layout:
    def __init__(self, shape):
        self.shape = shape
        self.stamps = []
        self.grabbed_stamp = None
        self.grabbed_type = None

    def getBaseStamp(self):
        if len(self.stamps) == 0:
            return None
        return self.stamps[0]

    def getStamps(self):
        stamps = []
        for stamp in self.stamps:
            stamps.append(stamp.copy())
        return stamps

    def newStamp(self, position=(0, 0), scale=(1.0, 1.0), angle=0):
        self.stamps.append(ShapeStamp(position, scale, angle))

    def removeStamp(self, stamp):
        if stamp in self.stamps:
            self.stamps.remove(stamp)

    # Get the stamp within range of the given point. If s is a stamp
    # then if will prefer to return that one if one isn't grabbed, otherwise
    # it it prefers the grabbed one.
    def getStamp(self, pos, s=None):
        if self.grabbed_stamp: # grabbed stamp has priority
            return self.grabbed_stamp
        if s: # then given stamp
            self.grabbed_type = s.pointWithin(pos, self.shape.bounds.size)
            if self.grabbed_type != None:
                return s
        for stamp in self.stamps:
            self.grabbed_type = stamp.pointWithin(pos, self.shape.bounds.size)
            if self.grabbed_type != None:
                return stamp
        return None

    def grabStamp(self, stamp):
        if stamp not in self.stamps: return
        for s in self.stamps:
            if stamp == s:
                stamp = s # use our reference, not theirs
                break
        self.grabbed_stamp = stamp

    def releaseStamp(self):
        self.grabbed_stamp = None

    def updateStamp(self, point, rel, snap=False, ratio=None):
        if not self.grabbed_stamp: return False
        if self.grabbed_type == ShapeStamp.TRANSLATE:
            if snap:
                self.grabbed_stamp.pos.x = point.x
                self.grabbed_stamp.pos.y = point.y
            else:
                self.grabbed_stamp.pos.x += rel.x
                self.grabbed_stamp.pos.y += rel.y
        elif self.grabbed_type == ShapeStamp.SCALE_TL:
            self._scale(point, rel, False, ratio)
        elif self.grabbed_type == ShapeStamp.SCALE_BR:
            self._scale(point, rel, True, ratio)
        elif self.grabbed_type == ShapeStamp.ROTATE_TR:
           self._rotate(point, rel, snap)
        elif self.grabbed_type == ShapeStamp.ROTATE_BL:
            self._rotate(point, rel, snap)
        return True

    def _getAngle(self, pos):
            if pos.x == 0:
                if pos.y > 0:
                    angle = 90
                else:
                    angle = 270
            else:
                angle = degrees(atan(pos.y / float(pos.x)))
                if pos.x < 0:
                    angle += 180
                elif pos.y < 0:
                    angle += 360
            return angle
        
    def _scale(self, point, rel, reverse, ratio):
        width = float(self.shape.bounds.width)
        height = float(self.shape.bounds.height)

        if ratio:
            old_r = self.grabbed_stamp.scale[1] / self.grabbed_stamp.scale[0]
            if old_r != ratio:
                self.grabbed_stamp.scale = (self.grabbed_stamp.scale[0], ratio *  self.grabbed_stamp.scale[0])
                print 'ratio:', self.grabbed_stamp.scale[1] / self.grabbed_stamp.scale[0]
            
        if reverse:
            anchor = Point(width/2 * self.grabbed_stamp.scale[0],
                           height/2 * self.grabbed_stamp.scale[1])
        else:
            anchor = Point(-width/2 * self.grabbed_stamp.scale[0],
                           -height/2 * self.grabbed_stamp.scale[1])
        anchor = Point.rotate(anchor, self.grabbed_stamp.angle)
        anchor.x += self.grabbed_stamp.pos.x
        anchor.y += self.grabbed_stamp.pos.y
        
        rel = Point(point.x - anchor.x, point.y - anchor.y)
        rel = Point.rotate(rel, -self.grabbed_stamp.angle)
        if ratio != None:
            a = self.grabbed_stamp.scale[0] > 0
            b = rel.x < rel.y
            c = reverse
            # No, this is not pretty. But I didn't like the alternative much
            # either. This reassigns either the x or y value such that
            # rel.y / rel.x = ratio, while also indirectly keeding the anchor
            # 'within' rel. This creates the expeceted behavior while resizing
            # and keeping the ratio, even when mirrored and flipped.
            if ((a and b and c) or (a and not b and not c) or
                (not a and b and not c) or (not a and not b and c)):
                rel.y = ratio * rel.x
            elif ((a and b and not c) or (a and not b and c) or
                  (not a and b and c) or (not a and not b and not c)):
                rel.x = 1 / ratio * rel.y

        dx = rel.x
        dy = rel.y
        if reverse:
            dx = -dx
            dy = -dy
        old_scale_x = self.grabbed_stamp.scale[0]
        old_scale_y = self.grabbed_stamp.scale[1]
        old_dx = width - old_scale_x * width
        old_dy = height - old_scale_y * height
        new_dx = old_dx + dx
        new_dy = old_dy + dy
        new_scale_x = (width - new_dx) / width
        new_scale_y = (height - new_dy) / height
        if abs(new_scale_x) > 0.1 and abs(new_scale_y) > 0.1:
            self.grabbed_stamp.scale = (new_scale_x, new_scale_y)
            if reverse:
                dx = -dx
                dy = -dy
            p = Point.rotate(Point(dx, dy), self.grabbed_stamp.angle)
            self.grabbed_stamp.pos.x += p.x / 2.0
            self.grabbed_stamp.pos.y += p.y / 2.0

    def _rotate(self, point, rel, snap):
        point.x -= self.grabbed_stamp.pos.x
        point.y -= self.grabbed_stamp.pos.y
        start_pos = Point(point.x - rel.x, point.y - rel.y)
        old_angle = self._getAngle(start_pos)
        new_vec = Point(start_pos.x + rel.x, start_pos.y + rel.y)
        new_angle = self._getAngle(new_vec)
        da = new_angle - old_angle
        angle = (self.grabbed_stamp.angle - da) % 360
        if snap:
            angle = round(angle)
        self.grabbed_stamp.angle = angle
