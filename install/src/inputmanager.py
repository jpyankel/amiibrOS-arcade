import pygame
from pathlib import Path
import configparser

root_path = (Path(__file__).parent.parent).resolve()
data_path = root_path / "data"
controller_path = data_path / "gamepads.config"

# tolerance before abs() of any joystick axis value is interpreted as 1 or -1
analog_tolerance = 0.5

class InputManager:
  def __init__(self):
    # load joystick config files from data/controllers.config
    self.gamepadConfigs = configparser.ConfigParser()
    self.gamepadConfigs.read(str(controller_path))

    # max number of joysticks is 4
    self.joysticks = []

    # list of "pretend" gamepads that hold processed values
    self.gamepads = []

    self.refreshJoysticks()

  def update(self, dt):
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        self.handleKeyboard(event)
      elif event.type in {pygame.JOYAXISMOTION, pygame.JOYHATMOTION,
                          pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP}:
        self.handleJoystick(event)

  def refreshJoysticks(self):
    # disconnect all connected joysticks from the event queue
    for j in self.joysticks:
      j.quit()
    self.joysticks.clear()

    # quit then init forces pygame.joystick to check if new joysticks are added
    #   or removed
    pygame.joystick.quit()
    pygame.joystick.init()

    # update list of connected joysticks
    # only enable the first 4 available joysticks
    for js_id in range(min(pygame.joystick.get_count(), 4)):
      joystick = pygame.joystick.Joystick(js_id)
      joystick.init()

      # add joystick to list of active joysticks
      self.joysticks.append(joystick)

      # try to configure virtual gamepad
      gamepad = GamePad(joystick.get_name(), self.gamepadConfigs)
      self.gamepads.append(gamepad)

  def handleKeyboard(self, event):
    if event.key == pygame.K_ESCAPE:
      pygame.quit() # TODO Handle gracefully
    elif event.key == pygame.K_r:
      print(self.gamepads)

  def handleJoystick(self, event):
    joystick = self.joysticks[event.joy]
    gamepad = self.gamepads[event.joy]

    if event.type == pygame.JOYAXISMOTION:
      if abs(event.value) > analog_tolerance:
        if event.value > 0:
          gamepad.setAJS(event.axis, 1)
        else:
          gamepad.setAJS(event.axis, -1)
      else:
          gamepad.setAJS(event.axis, 0)
    elif event.type == pygame.JOYHATMOTION:
      gamepad.setDJS(event.hat, event.value)
    elif event.type == pygame.JOYBUTTONDOWN:
      gamepad.setBTN(event.button, 1)
    else:
      # Event type is JOYBUTTONUP
      gamepad.setBTN(event.button, 0)

  def getConfiguredGamepadCount(self):
    count = 0

    for gamepad in self.gamepads:
      if gamepad.isConfigured():
        count += 1

    return count

class GamePad:
  def __init__(self, name, gamepadConfigs):
    # When configured, each of these holds a string out of the following:
    #   A, B, X, Y, L, R, Se, St
    self.btn_mapping = [None] * 12

    # When configured, each of these holds a string out of the following:
    #   AH1, AV1, AH2, AV2
    self.ajs_mapping = [None] * 4

    # When configured, each of these holds a string out of the following:
    #   D1, D2
    self.djs_mapping = [None] * 4

    self.current_btn = {
      "A" : False,
      "B" : False,
      "X" : False,
      "Y" : False,
      "L" : False,
      "R" : False,
      "Se" : False,
      "St" : False,
    }

    self.current_ajs = {
      "AH1" : 0,
      "AV1" : 0,
      "AH2" : 0,
      "AV2" : 0,
    }

    self.current_djs = {
      "D1" : (0, 0),
      "D2" : (0, 0),
    }

    self.configured = False

    self.configureInputMapping(name, gamepadConfigs)

  def configureInputMapping(self, name, gamepadConfigs):
    try:
      config = gamepadConfigs[name]
    except KeyError:
      # we cannot run setup
      return

    # map buttons
    for key in self.current_btn.keys():
      if key in config:
        self.btn_mapping[int(config[key])] = key

    # map analog joysticks
    for key in self.current_ajs.keys():
      if key in config:
        self.ajs_mapping[int(config[key])] = key

    # map digital joysticks
    for key in self.current_djs.keys():
      if key in config:
        self.djs_mapping[int(config[key])] = key

    self.configured = True

  def setBTN (self, btn, value):
    if not self.btn_mapping[btn]:
      return
    self.current_btn[self.btn_mapping[btn]] = value

  def setAJS (self, axis, value):
    if not self.ajs_mapping[axis]:
      return
    #print("Setting axis", axis, "(", self.ajs_mapping[axis], ") to", value)
    self.current_ajs[self.ajs_mapping[axis]] = value

  def setDJS (self, hat, value):
    if not self.djs_mapping[hat]:
      return
    #print("Setting hat", hat, "(", self.djs_mapping[hat], ") to", value)
    self.current_djs[self.djs_mapping[hat]] = value

  def isConfigured (self):
    return self.configured
