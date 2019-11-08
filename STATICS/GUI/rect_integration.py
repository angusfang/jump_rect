import pygame
from GUI.GUI_base.button_base import *
from GUI.rect_add import *
from GUI.rect_select import *
from GUI.element.element_side import ElementSide

import transformation as tra
import numpy as np


class RectIntegration():
    def __init__(self, b_surface: pygame.Surface):
        self.surface=b_surface
        self.button_size=50
        self.rect_list = [pygame.Rect]
        self.rect_add = RectAdd(b_surface,pygame.Rect((0,0),(self.button_size,self.button_size)))
        self.rect_select = RectSelect(b_surface,rect=pygame.Rect((0,self.button_size),(self.button_size,self.button_size)))
        self.even_list = []
        self.element_side_buf =ElementSide(np.eye(4))
        self.element_side_list = []


        x=b_surface.get_width()//2
        y=b_surface.get_height()//2
        vec4=[x,y,0,1]
        matrix4=tra.vec4_4_to_4x4(vec4)
        self.element_side_boundary=ElementSide(matrix4)
        # self.element_side_boundary.atom_size = 40
        self.element_side_boundary.create_boundary_atom_list(b_surface.get_width(),b_surface.get_height())
        self.element_side_boundary.rect=pygame.Rect((0,0),(b_surface.get_width(),b_surface.get_height()))
        self.element_side_boundary.rect.center=(b_surface.get_width()//2,b_surface.get_height()//2)


    def use(self):

        self.__share_event_list()

        self.rect_add.use()
        self.__up_other_status(self.rect_add)

        self.rect_list = self.rect_add.rect_list
        self.rect_select.rect_list = self.rect_list

        self.rect_select.use()
        self.__up_other_status(self.rect_select)

        self.__renew_element_side_list()
        self.__element_side_use()


        self.element_side_boundary.draw(self.surface)



    def __up_other_status(self,self_var):
        if self_var.status is Status.DOWN :
            self.rect_add.status =Status.UP
            self.rect_select.status =Status.UP
            self_var.status = Status.DOWN

    def __share_event_list(self):
        self.rect_select.even_list=self.even_list

    def __renew_element_side_list(self):
        if len(self.element_side_list) is not len(self.rect_list):
            self.element_side_list.clear()
            for rectI in self.rect_list:
                x=rectI.center[0]
                y=rectI.center[1]
                vec4=[x,y,0,1]
                m_4x4=tra.vec4_4_to_4x4(vec4)
                self.element_side_buf=ElementSide(m_4x4)
                self.element_side_buf.create_rect_atom_list(rectI.w, rectI.h)
                self.element_side_list.append(self.element_side_buf)
    def __element_side_use(self):

        for element_sideI in self.element_side_list:
            element_sideI:ElementSide
            element_sideI.draw(self.surface)
            element_sideI.cal_dynamic_and_move(self.element_side_list.index(element_sideI),self.element_side_list,self.element_side_boundary)
            pygame.draw.rect(self.surface,[0,0,50],element_sideI.rect)
