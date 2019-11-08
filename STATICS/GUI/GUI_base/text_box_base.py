import pygame
from tool.color import *
class TextBoxBase():
    def __init__(self,t_surface:pygame.Surface):
        self.surface=t_surface
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text='hello'
        self.text_format= self.font.render(self.text, True, black, white)
        self.textRect = self.text_format.get_rect()
        self.textRect.topleft = (self.surface.get_width()-self.textRect.w,0)

    def use(self):
        self.text_format = self.font.render(self.text, True, black, white)
        self.textRect = self.text_format.get_rect()
        self.textRect.topleft = (self.surface.get_width() - self.textRect.w, 0)
        self.surface.blit(self.text_format, self.textRect)