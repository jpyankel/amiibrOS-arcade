import pygame
from .drawable import Drawable, resource_path
from pathlib import Path
import math

scan_prompt_path = str(resource_path / "scan_prompt.png")

# period of transparency oscillation
# note the negative half of the sine-wave is clamped. So period is half on, half off
FADE_PERIOD = 2

class ScanPrompt(Drawable):
    def __init__(self, name, pos):
        super().__init__(name, pos)
        self.initPPA(scan_prompt_path)

        self.anim_time_elapsed = 0.0

    def draw(self, dt, parent, offset):
        if self.animating:
            self.anim_time_elapsed += dt

            # clamp to prevent animation jumping back during reset of self.anim_time_elapsed
            if self.anim_time_elapsed >= FADE_PERIOD:
                self.anim_time_elapsed = FADE_PERIOD

            # set transparency
            alpha_mult = max(0, math.sin(2*math.pi/FADE_PERIOD*self.anim_time_elapsed))
            self.setAlpha(alpha_mult*255)

            # to prevent float saturation (towards infinity), make sure to reset after each period
            # note this takes forever to notice, but we should try to be correct anyways
            if self.anim_time_elapsed == FADE_PERIOD:
                self.anim_time_elapsed = 0.0

        super().draw(dt, parent, offset)