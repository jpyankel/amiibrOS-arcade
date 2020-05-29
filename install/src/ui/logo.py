import pygame
from .uielement import UIElement, resource_path
from pathlib import Path

logo_path = str(resource_path / "title-logo.png")
tlogo_path = str(resource_path / "title-logo-transparent.png")

class Logo(UIElement):
  def __init__(self, pos):
    super().__init__(pos)
    self.switchToNonTransparent()

  def switchToTransparent(self):
    self.surface = pygame.image.load(tlogo_path)

  def switchToNonTransparent(self):
    self.surface = pygame.image.load(logo_path)
