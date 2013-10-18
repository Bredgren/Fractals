import pygame
from pygame.locals import *
from shape_window import ShapeWindow
from layout_window import LayoutWindow
from fractal_window import FractalWindow
from menu_window import MenuWindow
from geometry import Point

"""
Shape window controls:
left click - add new line or modify existing one
right click - remove line
control - hold to snap to grid or angles

Layout window controls:


Display window controls:
"""
class Main:
    BORDER_COLOR = pygame.Color('grey')
    BORDER_WIDTH = 5
    TEXT_COLOR = pygame.Color('white')
    FRACTAL_DISPLAY_SIZE = 600
    SIDE_DISPLAY_SIZE = (FRACTAL_DISPLAY_SIZE - BORDER_WIDTH) / 2
    MENU_HEIGHT = 150
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Fractals")

        self.setDisplay()
        self.plain_font = pygame.font.SysFont('Arial', 12)
        self.title_font = pygame.font.SysFont('Arial', 15)
        self.clock = pygame.time.Clock()

        self.shape_size_mod = 0
        self.layout_size_mod = 0
        
        self.running = True

    def setDisplay(self):
        width = self.display_width = (self.FRACTAL_DISPLAY_SIZE +
                                  self.SIDE_DISPLAY_SIZE +
                                  self.BORDER_WIDTH)
        height = self.display_height = (self.FRACTAL_DISPLAY_SIZE +
                                  self.MENU_HEIGHT +
                                  self.BORDER_WIDTH)
            
        self.display = pygame.display.set_mode((width, height))

        self.shape_window = ShapeWindow(self, 0, 0, self.SIDE_DISPLAY_SIZE)
        
        self.layout_window = LayoutWindow(self,
            0, self.SIDE_DISPLAY_SIZE + self.BORDER_WIDTH,
            self.SIDE_DISPLAY_SIZE, self.SIDE_DISPLAY_SIZE)
        
        self.fractal_window = FractalWindow(self,
            self.SIDE_DISPLAY_SIZE + self.BORDER_WIDTH, 0,
            self.FRACTAL_DISPLAY_SIZE, self.FRACTAL_DISPLAY_SIZE)
        
        self.menu_window = MenuWindow(self,
            0, self.SIDE_DISPLAY_SIZE*2 + self.BORDER_WIDTH*2,
            width, self.MENU_HEIGHT)

    def drawBorder(self):
        offset = self.SIDE_DISPLAY_SIZE + (self.BORDER_WIDTH-1) / 2.0
        pygame.draw.line(self.display, self.BORDER_COLOR,
                         (offset, 0),
                         (offset,
                          self.display.get_height() - self.MENU_HEIGHT - self.BORDER_WIDTH),
                         self.BORDER_WIDTH)
        
        pygame.draw.line(self.display, self.BORDER_COLOR,
                         (0, offset), (offset, offset),
                         self.BORDER_WIDTH)

        offset += self.SIDE_DISPLAY_SIZE + self.BORDER_WIDTH
        pygame.draw.line(self.display, self.BORDER_COLOR,
                         (0, offset), (self.display.get_width(), offset),
                         self.BORDER_WIDTH)
        
    def draw(self):
        self.shape_window.blitTo(self.display)
        self.layout_window.blitTo(self.display)
        self.fractal_window.blitTo(self.display)
        self.menu_window.blitTo(self.display)
        
        self.drawBorder()
        
        pygame.display.flip()

    def handleShapeDisplayLeftMouse(self, x, y):
        print "shape display left click ", x, y

    def handleShapeDisplayRightMouse(self, x, y):
        print "shape display right click ", x, y

    def handleLayoutDisplayLeftMouse(self, x, y):
        print "layout display left click ", x, y

    def handleLayoutDisplayRightMouse(self, x, y):
        print "layout display right click ", x, y

    def handleFractalDisplayLeftMouse(self, x, y):
        print "fractal dsiplay left click ", x, y

    def handleFractalDisplayRightMouse(self, x, y):
        print "fractal dsiplay right click ", x, y

    def handleMenuDisplayLeftMouse(self, x, y):
        print "menu display left click ", x, y

    def handleMenuDisplayRightMouse(self, x, y):
        print "menu display right click ", x, y

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = Point(event.pos[0], event.pos[1])
                if event.button == 1:
                    self.shape_window.handleLeftMouseDown(pos)
                    self.layout_window.handleLeftMouseDown(pos)
                    self.fractal_window.handleLeftMouseDown(pos)
                    self.menu_window.handleLeftMouseDown(pos)
                elif event.button == 3:
                    self.shape_window.handleRightMouseDown(pos)
                    self.layout_window.handleRightMouseDown(pos)
                    self.fractal_window.handleRightMouseDown(pos)
                    self.menu_window.handleRightMouseDown(pos)
            elif event.type == MOUSEBUTTONUP:
                pos = Point(event.pos[0], event.pos[1])
                if event.button == 1:
                    self.shape_window.handleLeftMouseUp(pos)
                    self.layout_window.handleLeftMouseUp(pos)
                    self.fractal_window.handleLeftMouseUp(pos)
                    self.menu_window.handleLeftMouseUp(pos)
                elif event.button == 3:
                    self.shape_window.handleRightMouseUp(pos)
                    self.layout_window.handleRightMouseUp(pos)
                    self.fractal_window.handleRightMouseUp(pos)
                    self.menu_window.handleRightMouseUp(pos)
            elif event.type == MOUSEMOTION:
                pos = Point(event.pos[0], event.pos[1])
                rel = Point(event.rel[0], event.rel[1])
                self.shape_window.handleMouseMove(pos, rel)
                self.layout_window.handleMouseMove(pos, rel)
                self.fractal_window.handleMouseMove(pos, rel)
                self.menu_window.handleMouseMove(pos, rel)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_LCTRL:
                    self.shape_window.snap_to_grid = True
                    self.layout_window.snap_to_grid = True
                elif event.key == K_LSHIFT:
                    self.layout_window.keep_current_ratio = True
                elif event.key == K_LALT:
                    self.layout_window.keep_original_ratio = True
                elif event.key == K_EQUALS:
                    self.shape_size_mod = 1
                elif event.key == K_MINUS:
                    self.shape_size_mod = -1
                elif event.key == K_KP_PLUS:
                    self.layout_size_mod = 1
                elif event.key == K_KP_MINUS:
                    self.layout_size_mod = -1
            elif event.type == KEYUP:
                if event.key == K_EQUALS:
                    self.shape_size_mod = 0
                elif event.key == K_LCTRL:
                    self.shape_window.snap_to_grid = False
                    self.layout_window.snap_to_grid = False
                elif event.key == K_LSHIFT:
                    self.layout_window.keep_current_ratio = False
                elif event.key == K_LALT:
                    self.layout_window.keep_original_ratio = False
                elif event.key == K_MINUS:
                    self.shape_size_mod = 0
                elif event.key == K_KP_PLUS:
                    self.layout_size_mod = 0
                elif event.key == K_KP_MINUS:
                    self.layout_size_mod = 0

        self.shape_window.grid_size += self.shape_size_mod
        self.layout_window.grid_size += self.layout_size_mod
        if self.shape_window.grid_size < 1:
           self.shape_window.grid_size = 1
        if self.layout_window.grid_size < 1:
            self.layout_window.grid_size = 1

        if self.shape_size_mod != 0:
            self.shape_window.dirty = True
            self.menu_window.dirty = True
        if self.layout_size_mod != 0:
            self.layout_window.dirty = True
            self.menu_window.dirty = True

    def saveSession(self):
        pass

    def loadSession(self):
        pass

    def saveImage(self):
        pass
        
    def run(self):
        while self.running:
            self.clock.tick(30)
            self.handleEvents()
            self.draw()
            
        pygame.quit()

if __name__ == "__main__":
    m = Main()
    m.run()
