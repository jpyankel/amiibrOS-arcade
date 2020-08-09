import pygame
from .drawable import Drawable
from .drawing_consts import *

class Background(Drawable):
    def __init__(self, name):
        super().__init__(name, (0, 0))
        self.surf = pygame.Surface(res)

        self.surf.fill(pygame.Color(defaultWhite))

        self.anim_time_elapsed = 0.0
        self.fade_b_w_dur = 0.0
        self.fade_b_w = False

    def playFadeBlackWhite(self, duration):
        self.animating = True

        self.anim_time_elapsed = 0.0
        self.fade_b_w_dur = duration
        self.fade_b_w = True

    def endFadeBlackWhite(self):
        self.fade_b_w = False

        self.surf.fill(pygame.Color(defaultWhite))

        self.animating = False

    def draw(self, dt, parent, offset):
        if self.fade_b_w and self.anim_time_elapsed < self.fade_b_w_dur:
            newColor = lerpColor(pygame.Color(defaultWhite), self.anim_time_elapsed,
                                 self.fade_b_w_dur)
            self.surf.fill(newColor)
            self.anim_time_elapsed += dt
        elif self.fade_b_w:
            self.endFadeBlackWhite()

        super().draw(dt, parent, offset)

def lerpColor (targetColor, currentValue, targetValue):
    interp = currentValue / targetValue

    r = targetColor.r * interp
    g = targetColor.g * interp
    b = targetColor.b * interp

    newColor = (r, g, b)

    return newColor