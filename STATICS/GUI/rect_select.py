import pygame
import enum
from GUI.GUI_base.button_base import *
from GUI.GUI_base.text_box_base import *
from GUI.element.force_add import *
from GUI.element.element import *


class RectSelect(ButtonBase):
    def __init__(self, b_surf: pygame.Surface, rect_list: [pygame.Rect] = [], rect=pygame.Rect((0, 400), (128, 256))):
        super().__init__(b_surf, rect)
        self.rect_list = rect_list
        self.rect = rect
        self.select_rect = -1
        self.select_status = Status.UP
        self.select_color = blue
        self.text_box = TextBoxBase(self.surface)

        self.element_buf = Element(-1)
        self.element_list: [Element] = [Element]
        self.element_list.clear()

    def function_down(self):
        left_click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_list:
            rect_ele: pygame.Rect
            for rect_ele in self.rect_list:
                if rect_ele.collidepoint(mouse_pos) and left_click is 1:
                    index = self.rect_list.index(rect_ele)
                    self.select_rect = index
                    self.select_status = Status.DOWN
        if self.select_status is Status.DOWN:
            if self.select_rect is not -1:
                self.__del_rect_function()
            if self.select_rect is not -1:
                self.text_box.text = str(self.select_rect)
                self.text_box.use()
                self.surface.fill(self.select_color, self.rect_list[self.select_rect])

        self.__renew_element_list()
        if self.select_status is Status.DOWN:
            if self.select_rect is not -1:
                ele_buf=self.element_list[self.select_rect]
                ele_buf.force_add.use()
    def function_up(self):
        self.select_status = Status.UP

    def __del_rect_function(self):

        for EV in self.even_list:
            if EV.type == pygame.KEYDOWN:
                if EV.key == pygame.K_d:
                    del (self.rect_list[self.select_rect])
                    self.select_rect = -1

    def __renew_element_list(self):
        if len(self.element_list) is not len(self.rect_list):
            self.element_list.clear()
            for rect_ele in self.rect_list:
                index = self.rect_list.index(rect_ele)
                self.element_buf = Element(self.surface, index)
                self.element_buf.force_add.limit_rect=rect_ele
                self.element_list.append(self.element_buf)

