import pygame
from .uielement import UIElement
from .drawingconst import *

class BG(UIElement):
  def __init__(self):
    super().__init__((0,0))
    self.surface = pygame.Surface(res)
    self.surface.fill(pygame.Color(defaultWhite))
