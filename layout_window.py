
import pygame
from window import Window
from layout import Layout

class LayoutWindow(Window):
    LINE_COLOR = pygame.Color('white')
    SELECT_COLOR = pygame.Color('yellow')
    BASE_COLOR = pygame.Color('light blue')
    def __init__(self, main, x, y, width, height=0):
        Window.__init__(self, main, x, y, width, height)
        self.grid_size = 10
        self.grid_visible = True
        self.selected_stamp = None
        self.snap_to_grid = False
        self.keep_current_ratio = False
        self.keep_original_ratio = False

        self.layout = Layout(self.main.shape_window.shape)
        self.colors = [pygame.Color('white')] * 10

    def setDirty(self):
        self.dirty = True
        self.main.fractal_window.setDirty()

    def updateSurface(self):
        self.fillBgd()
        if self.grid_visible:
            self.drawGrid()

        offset_x = self.rect.width / 2
        offset_y = self.rect.height / 2

        color = self.SELECT_COLOR
        # Draw the hightlight under the lines
        if self.selected_stamp:
            stamp = self.selected_stamp
            if stamp == self.layout.getBaseStamp():
                color = self.BASE_COLOR

            rect = self.main.shape_window.shape.bounds.copy()
            rect.width *= stamp.scale[0]
            rect.height *= stamp.scale[1]
            width_greater_than_zero = rect.width > 0
            height_greater_than_zero = rect.height > 0
            rect.width = abs(rect.width)
            rect.height = abs(rect.height)
            # give the lines some room
            rect.width += 3
            rect.height += 3
            half_width = rect.width / 2
            half_height = rect.height / 2
            rect.center = (half_width, half_height)
            if rect.width > 0 and rect.height > 0:
                temp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                pygame.draw.rect(temp, color, rect, 1)

                control_size = (stamp.control_size, stamp.control_size)
                rot_size = stamp.control_size / 2

                if width_greater_than_zero:
                    if height_greater_than_zero:
                        #s1 r1
                        #r2 s2
                        scale_pos1 = (0, 0)
                        scale_pos2 = (rect.width - control_size[0],
                                      rect.height - control_size[1])
                        rot_pos1 = (rect.width - control_size[0] + rot_size, rot_size)
                        rot_pos2 = (rot_size, rect.height - control_size[1] + rot_size)
                    else:
                        #r2 s2
                        #s1 r1
                        scale_pos1 = (0, rect.height - control_size[1])
                        scale_pos2 = (rect.width - control_size[0], 0)
                        rot_pos1 = (rect.width - control_size[0] + rot_size,
                                    rect.height - control_size[1] + rot_size)
                        rot_pos2 = (rot_size, rot_size)
                else:
                    if height_greater_than_zero:
                        #r1 s1
                        #s2 r2
                        scale_pos1 = (rect.width - control_size[0], 0)
                        scale_pos2 = (0, rect.height - control_size[1])
                        rot_pos1 = (rot_size, rot_size)
                        rot_pos2 = (rect.width - control_size[0] + rot_size,
                                    rect.height - control_size[1] + rot_size)
                    else:
                        #s2 r2
                        #r1 s1
                        scale_pos1 = (rect.width - control_size[0],
                                      rect.height - control_size[1])
                        scale_pos2 = (0, 0)
                        rot_pos1 = (rot_size, rect.height - control_size[1] + rot_size)
                        rot_pos2 = (rect.width - control_size[0] + rot_size, rot_size)

                scale_rect1 = pygame.Rect(scale_pos1, control_size)
                scale_rect2 = pygame.Rect(scale_pos2, control_size)
                pygame.draw.rect(temp, color, scale_rect1, 1)
                pygame.draw.rect(temp, color, scale_rect2, 1)
                pygame.draw.circle(temp, color, rot_pos1, rot_size, 1)
                pygame.draw.circle(temp, color, rot_pos2,rot_size, 1)
                                
                temp = pygame.transform.rotate(temp, stamp.angle)
                self.surface.blit(temp, ((self.surface.get_width() - temp.get_width()) / 2 + stamp.pos.x,
                                         (self.surface.get_height() - temp.get_height()) / 2 + stamp.pos.y))

        lines = self.main.shape_window.shape.getLines()
        shape_size = self.main.shape_window.shape.bounds.size
        for stamp in self.layout.getStamps():
            color = self.LINE_COLOR
            if stamp == self.layout.getBaseStamp():
                color = self.BASE_COLOR
            for line in lines:
                p1 = stamp.coords().applyCoords(line.point1)
                p2 = stamp.coords().applyCoords(line.point2)
                pygame.draw.line(self.surface, color,
                                 (p1.x + offset_x, p1.y + offset_y),
                                 (p2.x + offset_x, p2.y + offset_y))

        # Draw info over lines
        coords_str = "(,)"
        angle_str = "*"
        scale_str = "w: , h: "
        if self.selected_stamp:
            coords_str = "(%d, %d)" % (self.selected_stamp.pos.x, self.selected_stamp.pos.y)
            angle_str = "%.2f*" % (self.selected_stamp.angle)
            scale_str = "w: %.3f, h: %.3f" % (self.selected_stamp.scale)
            
        coords_text = self.main.plain_font.render(coords_str, 1,
                                                  self.main.TEXT_COLOR)

        
        angle_text = self.main.plain_font.render(angle_str, 1,
                                                self.main.TEXT_COLOR)

        
        scale_text = self.main.plain_font.render(scale_str, 1,
                                                self.main.TEXT_COLOR)
        
        self.surface.blit(coords_text, (0, 0))
        self.surface.blit(angle_text, (0, 20))
        self.surface.blit(scale_text, (0, 40))

##        ### Mouse position relative to rotated box for debuging
##        if len(self.layout.getStamps()) > 0:
##            p = self.localPoint(Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
##            p.x -= self.layout.getBaseStamp().pos.x
##            p.y -= self.layout.getBaseStamp().pos.y
##            p = Point.rotate(p, -self.layout.getBaseStamp().angle)
##            p.x += self.layout.getBaseStamp().pos.x
##            p.y += self.layout.getBaseStamp().pos.y
##            pygame.draw.circle(self.surface, pygame.Color('white'), (int(p.x+offset_x), int(p.y+offset_y)), 2)
##            self.setDirty()
        
    def handleLeftMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "layout display left down ", point.x, point.y
        if not self.selected_stamp:
            if self.snap_to_grid:
                point = self.snapToGrid(point)
            self.layout.newStamp(point)
            self.selected_stamp = self.layout.getStamp(point)
        self.layout.grabStamp(self.selected_stamp)
        self.setDirty()

    def handleRightMouseDown(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "layout display right down ", point.x, point.y
        if len(self.layout.stamps) > 0:
            self.layout.removeStamp(self.selected_stamp)
            self.selected_stamp = None
            self.setDirty()

    def handleLeftMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "layout display left up ", point.x, point.y
        self.layout.releaseStamp()

    def handleRightMouseUp(self, global_point):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "layout display right up ", point.x, point.y

    def handleMouseMove(self, global_point, rel):
        if not self.rect.collidepoint(global_point.x, global_point.y): return
        point = self.localPoint(global_point)
        print "layout display mouse move ", point.x, point.y, ":", rel.x, rel.y
        prev = self.selected_stamp
        self.selected_stamp = self.layout.getStamp(point, prev)

        if self.snap_to_grid:
            point = self.snapToGrid(point)

        ratio = None
        if self.keep_current_ratio and self.selected_stamp:
            ratio = self.selected_stamp.scale[1] / self.selected_stamp.scale[0]
        elif self.keep_original_ratio:
            ratio = 1
        print ratio

        if (self.layout.updateStamp(
                point, rel, self.snap_to_grid, ratio) or
                self.selected_stamp != prev):
            self.setDirty()
