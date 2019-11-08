import pygame
import numpy as np
from GUI.GUI_base.button_base import *
class SETPOS(enum.Enum):
    POS1 = 1
    POS2 = 2
    OVER = 3
class ForceAdd(ButtonBase):
    def __init__(self, b_surface: pygame.Surface, rect=pygame.Rect((0, 150), (50, 50))):
        super().__init__(b_surface, rect)
        self.__pos1 = (0, 0)
        self.__pos2 = (0, 0)
        self.__setpos = SETPOS.POS1
        self.__force_buf = (self.__pos1,self.__pos2)
        self.force_list = []
        self.down_color=[64,0,64]
        self.up_color=[96,0,96]
        self.limit_rect=rect
        self.fix_point=(rect.x,rect.y)

    def __setpos1(self, pos1):
        self.__pos1 = pos1

    def __setpos2(self, pos2):
        self.__pos2 = pos2

    def function_down(self):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if click[0] == 1:
            if self.__setpos == SETPOS.POS1 and self.limit_rect.collidepoint(mouse) :
                self.__setpos1(mouse)
                self.__setpos = SETPOS.POS2
            if self.__setpos == SETPOS.POS2:
                self.__setpos2(mouse)
                self.__force_buf = (self.__pos1,self.__pos2)

                pygame.draw.line(self.surface,[127,127,0],self.__force_buf[0],self.__force_buf[1],1)
                pygame.draw.circle(self.surface, [127, 127, 0],self.__force_buf[1], 5)
        if click[0] == 0 and self.__setpos == SETPOS.POS2:
            self.__setpos = SETPOS.OVER
            self.force_list.append(self.__force_buf)
        if self.__setpos == SETPOS.OVER:
            self.__setpos = SETPOS.POS1
        if self.force_list:
            for forceI in self.force_list:
                pygame.draw.line(self.surface,[65,65,0], forceI[0], forceI[1], 1)
                pygame.draw.circle(self.surface,[65,65,0],forceI[1],5)

        pygame.draw.circle(self.surface, [255, 0, 0], self.fix_point, 5)

    def function_up(self):
        for forceI in self.force_list:
            pygame.draw.line(self.surface, [65, 65, 0], forceI[0], forceI[1], 1)
            pygame.draw.circle(self.surface, [65, 65, 0], forceI[1], 5)

        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if click[0] == 1 and self.limit_rect.collidepoint(mouse):
            self.fix_point=mouse
        pygame.draw.circle(self.surface, [255, 0, 0], self.fix_point, 5)