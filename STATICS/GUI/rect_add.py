import pygame
import enum
from GUI.GUI_base.button_base import *


class SETPOS(enum.Enum):
    POS1 = 1
    POS2 = 2
    OVER = 3


class RectAdd(ButtonBase):
    def __init__(self, b_surface: pygame.Surface,rect=pygame.Rect((0,0),(128,128))):
        super().__init__(b_surface,rect)
        self.__pos1 = (0, 0)
        self.__pos2 = (0, 0)
        self.__setpos = SETPOS.POS1
        self.__rect_buf = pygame.Rect
        self.rect_list: [pygame.Rect] = []

    def __setpos1(self, pos1):
        self.__pos1 = pos1

    def __setpos2(self, pos2):
        self.__pos2 = pos2

    def function_down(self):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if click[0] == 1:
            if self.__setpos == SETPOS.POS1:
                self.__setpos1(mouse)
                self.__setpos = SETPOS.POS2
            if self.__setpos == SETPOS.POS2:
                self.__setpos2(mouse)
                self.__rect_buf = pygame.Rect(self.__pos1[0], self.__pos1[1], self.__pos2[0] - self.__pos1[0],
                                              self.__pos2[1] - self.__pos1[1])
                self.__rect_buf.normalize()
                self.surface.fill(blue, self.__rect_buf)
        if click[0] == 0 and self.__setpos == SETPOS.POS2:
            self.__setpos = SETPOS.OVER
            self.rect_list.append(self.__rect_buf)
        if self.__setpos == SETPOS.OVER:
            self.__setpos = SETPOS.POS1
        # if self.rect_list:
        #     for rectI in self.rect_list:
        #         self.surface.fill(black, rectI)

    def function_up(self):
        # if self.rect_list:
        #     for rectI in self.rect_list:
        #         self.surface.fill(black, rectI)
        pass

if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    surfRect = surface.get_rect()

    button1 = RectAdd(surface)
    button1.rect.topleft = (0, 0)

    touch = False
    while True:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                quit()
            surface.fill(red)
            button1.use()

            surface.fill(button1.color, button1.rect)

            pygame.display.flip()
