import pygame
from .drawable import Drawable, resource_path
from pathlib import Path

scanner_path_str = str(resource_path / "scanner.png")

class ScannerIcon(Drawable):
    def __init__(self, name, pos):
        super().__init__(name, pos)

        self.initPPA(scanner_path_str)

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
