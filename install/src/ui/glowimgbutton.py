import pygame
from .uielement import UIElement, resource_path
from pathlib import Path

button_path = resource_path / "button"

# TODO Needs a base image and a glow image
# Will need to load both images.
# Glow image opacity can be set with special functions belonging to this subclass

class GlowImageButton(UIElement):
  def __init__(self, pos, name, imgbasename):
    super().__init__(pos, name)
    path = button_path / (imgbasename + "-reg.png")
    self.initPPA(str(path))

    glowpath = button_path / (imgbasename + "-glow.png")
    self.glowFX = UIElement((0, 0), "%s-glow" % (imgbasename))
    self.glowFX.initPPA(str(glowpath))

    # start as deselected and unhovered
    self.glowFX.setAlpha(0)

    self.addChild(self.glowFX)

  def hover(self):
    # TODO Increase opacity of glow
    # Play translate animation
    pass

  def unhover(self):
    # TODO Decrease opacity of glow
    # Play translate back animation
    pass

  def select(self):
    # TODO Increase opacity of glow
    # Play button click down animation
    pass

  def deselect(self):
    # TODO Decrease opacity of glow
    # Play button click up animation
    pass
