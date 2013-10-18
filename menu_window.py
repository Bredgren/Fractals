
import pygame
from window import Window

class MenuWindow(Window):
    def __init__(self, main, x, y, width, height=0):
        Window.__init__(self, main, x, y, width, height)

    def updateSurface(self):
        self.fillBgd()
        
        surface = self.surface
        main = self.main

        shape_title_str = "Shape Window"
        shape_title_text = main.title_font.render(shape_title_str, 1,
                                                  main.TEXT_COLOR)
        surface.blit(shape_title_text, (10, 10))

        grid_size = main.shape_window.grid_size
        shape_grid_str = "Grid size: %d px" % grid_size
        shape_grid_text = main.plain_font.render(shape_grid_str, 1,
                                                 main.TEXT_COLOR)
        surface.blit(shape_grid_text, (10, 30))

        layout_title_str = "Layout Window"
        layout_title_text = main.title_font.render(layout_title_str, 1,
                                                  main.TEXT_COLOR)
        surface.blit(layout_title_text, (300, 10))
        
        grid_size = main.layout_window.grid_size
        layout_grid_str = "Grid size: %d px" % grid_size
        layout_grid_text = main.plain_font.render(layout_grid_str, 1,
                                                  main.TEXT_COLOR)
        surface.blit(layout_grid_text, (300, 30))

        fractal_title_str = "Display Window"
        fractal_title_text = main.title_font.render(fractal_title_str, 1,
                                                    main.TEXT_COLOR)
        surface.blit(fractal_title_text, (600, 10))

    def handleLeftMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "menu display left down ", point.x, point.y

    def handleRightMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "menu display right down ", point.x, point.y

    def handleLeftMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "menu display left up ", point.x, point.y

    def handleRightMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "menu display right up ", point.x, point.y

    def handleMouseMove(self, global_point, rel):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "menu display mouse move ", point.x, point.y, ":", rel.x, rel.y
