import pygame
from pygame.locals import *
from tool.color import *
from  GUI.rect_integration import *
from GUI.GUI_base.text_box_base import *

if __name__ == '__main__':

    pygame.init()
    surface = pygame.display.set_mode((1400, 800))
    clock = pygame.time.Clock()
    surfRect = surface.get_rect()

    buttonI=RectIntegration(surface)
    text1=TextBoxBase(surface)

    touch = False
    while True:
        event_list=pygame.event.get()
        for EV in event_list:
            if EV.type == pygame.KEYDOWN:
                if EV.key == pygame.K_ESCAPE:
                    quit()

        surface.fill(white)
        buttonI.even_list=event_list

        buttonI.use()
        # text1.use()

        if buttonI.rect_select.select_rect is not -1:
          # print(buttonI.rect_list[buttonI.rect_select.select_rect].collidelistall(buttonI.rect_list))
          # print(buttonI.rect_list[buttonI.rect_select.select_rect].center)
         pass
        pygame.display.flip()


