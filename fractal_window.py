
import pygame
from window import Window
from geometry import Coords, Point, Line
from itertools import chain

import time
current_time = lambda: int(round(time.time() * 1000)) #ms

class FractalWindow(Window):
    LINE_COLOR = pygame.Color('white')
    def __init__(self, main, x, y, width, height=0):
        Window.__init__(self, main, x, y, width, height)
        self.shape = self.main.shape_window.shape
        self.layout = self.main.layout_window.layout
        self.check_point = None
        # This is the maximum number of milliseconds that this window has
        # to draw during each frame. If the time is exceeded it remembers
        # where it was and resumes in the next frame.
        self.time_limit = 50
        self.end_time = 0
        self.min_line_size = 0.05
        self.colors = self.main.layout_window.colors

    def setDirty(self):
        self.dirty = True
        self.check_point = None

    def updateSurface(self):
        if not self.check_point:
            self.fillBgd()

        offset_x = self.rect.width / 2
        offset_y = self.rect.height / 2

        def drawStamp(stamp, coords, color=self.LINE_COLOR):
            max_size = 0
            for line in self.shape.lines:
                p1 = stamp.coords().applyCoords(line.point1)
                p2 = stamp.coords().applyCoords(line.point2)

                p1 = coords.applyCoords(p1)
                p2 = coords.applyCoords(p2)
                size = Line(p1, p2).length()
                max_size = max(max_size, size)
                
                if ((-offset_x < p1.x < offset_x and  -offset_y < p1.y < offset_y) or
                    (-offset_x < p2.x < offset_x and  -offset_y < p2.y < offset_y)):
                    pygame.draw.line(self.surface, color,
                                     (p1.x + offset_x, p1.y + offset_y),
                                     (p2.x + offset_x, p2.y + offset_y))
            return max_size

        # Recursively draws the layout at each of the Coords specified.
        # this_depth_count is the number of coordinates in coords that
        # correspond with the given depth, while next_depth_count is the
        # number of coordinates in coords that correspond to depth-1.
        # There should never be any other coordinates corresponding to
        # any other depth.
        def drawLayout(coords, this_depth_count, next_depth_count, depth):
            non_base_stamps = self.layout.getStamps()[1:]
            def getCoords(c):
                for stamp in non_base_stamps:
                    yield c.shiftCoords(stamp.coords())
                    
            if depth <= 0:
                self.check_point = None
                return
            
            new_coords = iter([])
            m = 0
            count = 1
            for coord in coords:
                for stamp, color in zip(non_base_stamps, self.colors):
                    s = drawStamp(stamp, coord, color)
                    m = max(m, s)
                new_coords = chain(new_coords, getCoords(coord))
                next_depth_count += len(non_base_stamps)
                if current_time() > self.end_time:
                    c = chain(coords, new_coords)
                    if count == this_depth_count:
                        # exhasted all coords for this depth, move on to next on next frame.
                        self.check_point = (c, next_depth_count, 0, depth-1)
                    else:
                        # did not finish drawing this depth.
                        self.check_point = (c, this_depth_count - count, next_depth_count, depth)
                    return
                if count == this_depth_count:
                    # exhasted all coords for this depth and we still have time left.
                    break
                count += 1
            if m < self.min_line_size:
                # don't go any deeper because the lines are too small.
                self.check_point = None
                return
            drawLayout(new_coords, next_depth_count, 0, depth-1)

        if len(self.layout.getStamps()) > 0:
            self.end_time = current_time() + self.time_limit
            if self.check_point:
                # resume where we left off
                coords = self.check_point[0]
                t_d_c = self.check_point[1]
                n_d_c = self.check_point[2]
                depth = self.check_point[3]
                self.check_point = None
                drawLayout(coords, t_d_c, n_d_c, depth)
            else:
                # start over
                base_stamp = self.layout.getBaseStamp()
##                start = Coords(Point(0,0), (1.0, 1.0), 0)
                start = base_stamp.coords()
                drawStamp(base_stamp, start)
                drawLayout(iter([start]), 1, 0, 50)

            if self.check_point:
                self.dirty = True

    def handleLeftMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "fractal display left down ", point.x, point.y

    def handleRightMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "fractal display right down ", point.x, point.y

    def handleLeftMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "fractal display left up ", point.x, point.y

    def handleRightMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "fractal display right up ", point.x, point.y

    def handleMouseMove(self, global_point, rel):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "fractal display mouse move ", point.x, point.y, ":", rel.x, rel.y
