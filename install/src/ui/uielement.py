import pygame
from pathlib import Path

# path to resources folder; various images/fonts are stored here
root_path = (Path(__file__).parent.parent.parent).resolve()
resource_path = root_path / "resources"

class UIElement():
  def __init__(self, pos):
    self.pos = pos

    # the main surface for this UI element (sub-objects will be drawn in front)
    # subclasses must populate this before returning
    self.surface = None

    # contains other UI subclasses
    self.children = []

  def draw(self, parent, offset):
    """ Draw this UI element and its sub-elements onto parent surface.
    parent: parent surface (pygame.Surface)
    offset: parent surface (x,y) position (tuple)
    """
    # draw this surface onto parent
    new_pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
    parent.blit(self.surface, new_pos)

    # tell other sub-objects to draw onto this surface
    for child in self.children:
      child.draw(self.surface, new_pos)

  def fadeIn(self, te, td):
    """ Fades in opacity proportional to time elapsed.
    te: current time elapsed
    td: transition duration
    """
    self.surface.set_alpha(te/td*255)

  def fadeOut(self, te, td):
    """ Fades out opacity proportional to time elapsed.
    te: current time elapsed
    td: transition duration
    """
    self.surface.set_alpha((1-te/td)*255)

  def setAlpha(self, alpha):
    self.surface.set_alpha(alpha)

  def addChild(self, child):
    """ Adds a child object to this UI elements sub-objects list.
    Sub-objects are drawn in front when draw() is called, and are positioned
    relative to the parent.
    """
    self.children.append(child)
