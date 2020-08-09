import pygame
from drawables.drawing_consts import *


class DrawManager:
    def __init__(self):
        # the "screen" surface to draw to
        self.screen = pygame.display.set_mode(res, pygame.FULLSCREEN)

        # font used to render FPS or other debug stats
        self.stat_font = pygame.font.Font(None, 30)
        self.stat_color = pygame.Color("black")

        self.reset()

    def update(self, dt, fps):
        # draw all scene objects
        for drawable in self.drawables:
            drawable.draw(dt, self.screen, (0, 0))

        if fps != None:
            fps_overlay = self.stat_font.render(str(int(fps)), True, self.stat_color)
            # draw FPS average overlay
            self.screen.blit(fps_overlay, (10,0))

        # write all changes to the screen
        pygame.display.update()

    def addDrawable(self, d):
        self.drawables.append(d)

    def reset(self):
        # list of objects in the order they are drawn
        self.drawables = []