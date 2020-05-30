import pygame
from .uielement import UIElement
from .drawingconst import *

class BG(UIElement):
  def __init__(self, name):
    super().__init__((0,0), name)
    self.surf = pygame.Surface(res)
    self.surf.fill(pygame.Color(defaultWhite))
