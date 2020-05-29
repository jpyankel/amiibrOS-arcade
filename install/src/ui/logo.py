import pygame
from .uielement import UIElement, resource_path
from pathlib import Path

logo_path = str(resource_path / "fullscreen-logo.png")

class Logo(UIElement):
  def __init__(self, pos):
    super().__init__(pos)
    self.surface = pygame.image.load(logo_path)
