import pygame
from .uielement import UIElement, resource_path
from pathlib import Path

button_path = resource_path / "button"

class ImageButton(UIElement):
  def __init__(self, pos, name, imgname):
    super().__init__(pos, name)
    self.imgname = None
    self.setImage(imgname)

  def setImage(self, imgname):
    self.imgname = imgname
    path = button_path / (imgname + "-reg.png")
    self.surf = pygame.image.load(str(path))

  def select(self):
    path = button_path / (imgname + "-sel.png")
    self.surf = pygame.image.load(str(path))

  def deselect(self):
    path = button_path / (imgname + "-reg.png")
    self.surf = pygame.image.load(str(path))
