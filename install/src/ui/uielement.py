import pygame
from pathlib import Path

# path to resources folder; various images/fonts are stored here
root_path = (Path(__file__).parent.parent.parent).resolve()
resource_path = root_path / "resources"

class UIElement():
  def __init__(self, pos, name):
    # identifier for debugging
    self.name = name

    # holds the position, this is used to track the offset for child elements
    self.pos = pos

    # the main surface for this element (sub-objects will be drawn in front).
    # subclasses must populate this before returning from __init__().
    self.surf = None

    # contains other UI subclasses.
    self.children = []

    # determines if we should use the more expensive drawing method.
    # enabling will force draw() to combine per-pixel alpha and surface alpha.
    self.ppa_render = False

    # if the previous is true, then the following surface holds our per-pixel
    #   alpha image. self.surface will hold a blank background with a target
    #   global transparency.
    # initialized by subclass by using initPPA
    self.ppa_surf = None

  def draw(self, parent, offset):
    """ Draw this UI element and its sub-elements onto parent surface.
    parent: parent surface (pygame.Surface)
    offset: parent surface (x,y) position (tuple)
    """
    # calculate this element's offset from its parent
    new_pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
    print("parent!", self.name)

    if self.ppa_render:
      copy_img = self.ppa_surf.copy()
      copy_img.blit(self.surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
      # draw the copy surface onto the parent surface
      parent.blit(copy_img, new_pos)
      # tell other sub-objects to draw onto the copy surface, to be drawn later
      #   onto the parent surface
      for child in self.children:
        child.draw(parent, new_pos)
    else:
      # draw this surface onto the parent surface
      parent.blit(self.surf, new_pos)
      # tell other sub-objects to draw onto the parent overtop this one
      for child in self.children:
        child.draw(parent, new_pos)

  def fadeIn(self, te, td):
    """ Fades in opacity proportional to time elapsed.
    te: current time elapsed
    td: transition duration
    """
    self.setAlpha(te/td*255)

  def fadeOut(self, te, td):
    """ Fades out opacity proportional to time elapsed.
    te: current time elapsed
    td: transition duration
    """
    self.setAlpha((1-te/td)*255)

  def setAlpha(self, alpha):
    """ Sets alpha value to alpha"""
    if self.ppa_render:
      self.surf.fill( (255,255,255,alpha) )
    else:
      self.surf.set_alpha(alpha)

  def initPPA(self, imgpath):
    """ Forces draw() to use a more expensive blit() operation enabling the
        combination of per-pixel-alpha and set_alpha().

      imgpath: the path to the image to load with per-pixel-alpha
    """
    self.ppa_surf = pygame.image.load(imgpath).convert_alpha()
    self.surf = pygame.Surface(self.ppa_surf.get_rect().size, pygame.SRCALPHA)

    self.ppa_render = True

    # start out at 100% opacity
    self.setAlpha(255)

  def addChild(self, child):
    """ Adds a child object to this UI elements sub-objects list.
    Sub-objects are drawn in front when draw() is called, and are positioned
    relative to the parent.
    """
    self.children.append(child)
