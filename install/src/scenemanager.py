import pygame
from .inputmanager import InputManager
from .ui.drawingconst import *

class SceneManager:
  def __init__(self):
    # the "screen" surface to draw to
    self.screen = pygame.display.set_mode(res, pygame.FULLSCREEN)

    # current scene object
    self.scene = None

    # input manager
    self.input_mgr = InputManager()

    # transitioning state. in this state, no inputs are processed.
    self.transitioning = False

    # determines which transition animation to play
    self.tID = None

    # elasped time in the current transition
    self.tET = 0.0

    self.font = pygame.font.Font(None, 30)

  def update(self, dt, fps):
    """ Updates the input manager to receive the latest inputs, then performs
    scene specific logic, then draws the scene to the screen.

    dt: delta-time, or time between this frame and its predecessor [ms]
    """

    # update current inputs
    self.input_mgr.update(dt)

    if self.transitioning:
      if self.scene != None:
        if self.scene.playTransition(self.transitionID, self.te):
          self.endTransition()
      else:
        # this occurs when starting the first scene
        self.endTransition()

      self.tET += dt
    else:
      self.scene.checkLogic(self.input_mgr, dt)

    self.scene.draw(self.screen)

    if fps != None:
      fps_overlay = self.font.render(str(int(fps)), True, pygame.Color("black"))
      # draw FPS average overlay
      self.screen.blit(fps_overlay, (10,0))

    pygame.display.update()

  def loadScene(self, next_scene, transitionID=0):
    # begins the transition to the next scene
    self.transitioning = True
    self.next_scene = next_scene
    self.tID = transitionID
    self.tET = 0.0 # TODO Make transition elapsed time handled by the scene

  def endTransition(self):
    self.transitioning = False # TODO get rid of transitioning variable and just use next_scene
    self.scene = self.next_scene
    self.next_scene = None
