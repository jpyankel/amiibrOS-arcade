import pygame
from .drawable import Drawable
from .drawing_consts import *

class FadeOutForeground(Drawable):
    def __init__(self, name):
        super().__init__(name, (0, 0))

        self.ppa_surf = pygame.Surface(res, pygame.SRCALPHA)
        self.ppa_surf.fill(pygame.Color("black"))
        self.surf = pygame.Surface(self.ppa_surf.get_rect().size, pygame.SRCALPHA)
        self.ppa_render = True
        self.setAlpha(0)

        self.anim_time_elapsed = 0.0
        self.fade_dur = 0.0
        self.fade_in = False

    def playFadeIn(self, duration):
        self.animating = True

        self.anim_time_elapsed = 0.0
        self.fade_dur = duration
        self.fade_in = True

    def endFadeIn(self):
        self.fade_in = False

        self.setAlpha(255)

        self.animating = False

    def draw(self, dt, parent, offset):
        if self.fade_in and self.anim_time_elapsed < self.fade_dur:
            self.fadeIn(self.anim_time_elapsed, self.fade_dur)
            self.anim_time_elapsed += dt
        elif self.fade_in:
            self.endFadeIn()

        super().draw(dt, parent, offset)