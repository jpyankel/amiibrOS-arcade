import pygame
from pathlib import Path
import configparser

root_path = (Path(__file__).parent.parent).resolve()
data_path = root_path / "data"
controller_path = data_path / "controller.config"

# tolerance before abs() of any joystick axis value is interpreted as 1 or -1
analog_tolerance = 0.5

class InputManager:
  def __init__(self):
    # this should be updated every frame.
    # this depends on the controller's configuration as well as current inputs
    self.processedInputs = {
      "A" : False,
      "B" : False,
      "X" : False,
      "Y" : False,
      "Se" : False,
      "St" : False,
      "Ve" : 0,
      "Ho" : 0
    }

    # the first joystick ID that inputs an action gets to control the interface
    self.primary_id = None

    # should we poll to find the primary joystick?
    self.set_primary = True

    # load joystick config files from data/controllers.config
    self.gamepadConfigs = configparser.ConfigParser().read(str(controller_path))

    self.joysticks = []

    self.refreshJoysticks()

  def update(self, dt):
    if self.set_primary:
      print("FINDING JOYSTICKS")
      # Poll any event for the first joystick
      for joystick in self.joysticks:
        if joystickAnyInput(joystick):
          self.primaryID = joystick.get_id()
          self.set_primary = False
          print("JOYSTICK FOUND: ", self.joysticks[self.primaryID].get_name())
    elif self.primary_id != None:
      # Update currently pressed stuff
      pass

    # TODO replace with pygame.event.pump() when we reimplement the below functionality
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit() # TODO HANDLE GRACEFULLY

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit() # TODO REMOVE

  def refreshJoysticks(self):
    # the primary controller will need to be chosen again
    self.primary_id = None

    # quit then init forces pygame.joystick to check if new joysticks are added
    #   or removed
    pygame.joystick.quit()
    pygame.joystick.init()

    # update list of connected joysticks
    for js_id in range(pygame.joystick.get_count()):
      joystick = pygame.joystick.Joystick(js_id)
      joystick.init()
      self.joysticks.append(joystick)

  def resetPrimary (self):
    self.primary_id = None
    self.set_primary = True

  def hasPrimary (self):
    return self.primary_id != None

def joystickAnyInput(joystick):
  """ Returns True if any joystick button or other input is not 0 """

  # check all buttons
  for btn_id in range(joystick.get_numbuttons()):
    if joystick.get_button(btn_id):
      return True

  # check all analog joysticks
  for ajs_id in range(joystick.get_numaxes()):
    if abs(joystick.get_axis(ajs_id)) >= analog_tolerance:
      return True

  # check all "digital" joysticks
  for djs_id in range(joystick.get_numhats()):
    if joystick.get_hat(djs_id) != (0, 0):
      return True

  return False
