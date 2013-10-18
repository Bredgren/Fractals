
import pygame
from window import Window
from shape import Shape
from geometry import Point

class ShapeWindow(Window):
    LINE_COLOR = pygame.Color('white')
    SELECT_COLOR = pygame.Color('yellow')
    def __init__(self, main, x, y, width, height=0):
        Window.__init__(self, main, x, y, width, height)
        self.grid_size = 10
        self.grid_visible = True
        self.selected_point = None
        self.snap_to_grid = False

        self.shape = Shape()

    def setDirty(self):
        self.dirty = True
        self.main.layout_window.setDirty()

    def updateSurface(self):
        self.fillBgd()
        if self.grid_visible:
            self.drawGrid()
            
        offset_x = self.rect.width / 2
        offset_y = self.rect.height / 2
        
        for line in self.shape.getLines():
            pygame.draw.line(self.surface, self.LINE_COLOR,
                             (line.point1.x + offset_x,
                              line.point1.y + offset_y),
                             (line.point2.x + offset_x,
                              line.point2.y + offset_y))

        if self.selected_point:
            x = self.selected_point.x + offset_x
            y = self.selected_point.y + offset_y
            pygame.draw.circle(self.surface, self.SELECT_COLOR,
                               (x, y), 5, 1)
            coords_str = "(%d, %d)" % (x-offset_x, y-offset_y)
            coords_text = self.main.plain_font.render(coords_str, 1,
                                                      self.main.TEXT_COLOR)
            s = self.main.plain_font.size(coords_str)
            x -= s[0] / 2
            if x < 0:
                x = 0
            elif x > self.surface.get_width() - s[0]:
                x = self.surface.get_width() - s[0]
            offset = 20
            y -= offset
            if y < 0:
                y += 2*offset
            self.surface.blit(coords_text, (x, y))

    def handleLeftMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "shape display left down ", point.x, point.y
        if not self.selected_point:
            if self.snap_to_grid:
                point = self.snapToGrid(point)
            p2 = Point(point.x, point.y)
            self.shape.newLine(point, p2)
            self.shape.grabPoint(point)
            self.selected_point = self.shape.getPoint(point)
        self.shape.grabPoint(self.selected_point)
        self.setDirty()

    def handleRightMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "shape display right down ", point.x, point.y
        if len(self.shape.lines) > 0:
            self.shape.removeLine(self.selected_point)
            self.selected_point = None
            self.setDirty()

    def handleLeftMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "shape display left up ", point.x, point.y
        self.shape.releasePoint()

    def handleRightMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "shape display right up ", point.x, point.y

    def handleMouseMove(self, global_point, rel):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "shape display mouse move ", point.x, point.y, ":", rel.x, rel.y
        prev = self.selected_point
        self.selected_point = self.shape.getPoint(point)

        if self.snap_to_grid:
            point = self.snapToGrid(point)
                    
        if self.shape.updatePoint(point) or self.selected_point != prev:
            self.setDirty()
