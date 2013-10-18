
import pygame
from geometry import Point

class Window:
    DEFAULT_BGD_COLOR = pygame.Color('black')
    DEFAULT_GRID_COLOR = pygame.Color(50, 50, 50)
    def __init__(self, main, x, y, width, height=0):
        if height == 0:
            height = width
        self.main = main
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self.bgd_color = self.DEFAULT_BGD_COLOR
        self.grid_color = self.DEFAULT_GRID_COLOR
        self.dirty = True
        
    def setDirty(self):
        self.dirty = True
        if self.blit_process and self.blit_process.is_alive():
            self.blit_process.terminate()
        self.blit_process = None

    def fillBgd(self):
        self.surface.fill(self.bgd_color)

    def updateSurface(self):
        raise NotImplementedError("This method has not been implemented yet")
        
    def blitTo(self, surface):
        if self.dirty:
            self.dirty = False
            self.updateSurface()
        surface.blit(self.surface, self.rect)

    def drawGrid(self):
        width = self.surface.get_width()
        center = width / 2
        offset = map(lambda x: x - center,
                     range(center % self.grid_size, width, self.grid_size))
        for x in offset:
            pygame.draw.line(self.surface, self.grid_color,
                         (x + center, 0), (x + center, width))
        for y in offset:
            pygame.draw.line(self.surface, self.grid_color,
                         (0, y + center), (width, y + center))

    def snapToGrid(self, point):
        snap_point = Point(point.x, point.y)
        width = self.surface.get_width()
        center = width / 2
        half = self.grid_size / 2
        offset = map(lambda x: x - center,
                     range(center % self.grid_size, width, self.grid_size))
        possible_x = range(point.x - half, point.x + half)
        possible_y = range(point.y - half, point.y + half)
        for x in possible_x:
            if x in offset:
                snap_point.x = x
                break
        for y in possible_y:
            if y in offset:
                snap_point.y = y
                break
        return snap_point

    def localPoint(self, global_point):
        local_point = Point()
        local_point.x = global_point.x - self.rect.left - self.rect.width / 2
        local_point.y = global_point.y - self.rect.top - self.rect.height / 2
        return local_point

    def handleLeftMouseDown(self, global_point):
        raise NotImplementedError("This method has not been implemented yet")

    def handleRightMouseDown(self, global_point):
        raise NotImplementedError("This method has not been implemented yet")

    def handleLeftMouseUp(self, global_point):
        raise NotImplementedError("This method has not been implemented yet")

    def handleRightMouseUp(self, global_point):
        raise NotImplementedError("This method has not been implemented yet")

    def handleMouseMove(self, global_point, rel):
        raise NotImplementedError("This method has not been implemented yet")
