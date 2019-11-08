import pygame
from GUI.element.force_add import *

class Element():
    def __init__(self,b_surface: pygame.Surface,id=-1):
        self.id=id
        self.force_add=ForceAdd(b_surface)

