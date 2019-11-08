import pygame
from tool import color


class Rect:
    def __init__(self, x, y, w, h, col=color.blue):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = col

    def use(self,gameDisplay):
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.width, self.height))

    def if_inside(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return True
        else:
            return False


if __name__ == "__main__":

    display_width = 900
    display_height = 900

    pygame.init()
    clock = pygame.time.Clock()
    gameDisplay = pygame.display.set_mode((display_width, display_height))

    b1 = Rect(450, 450, 50, 50)
    b1.if_inside(460, 460)
    b1.use()

    while (1):
        clock.tick(150)

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(color.black)

        pygame.display.update()
