import pygame
from pathlib import Path
import configparser

root_path = (Path(__file__).parent.parent).resolve()
data_path = root_path / "data"
controller_path = data_path / "gamepads.config"

# tolerance before abs() of any joystick axis value is interpreted as 1 or -1
analog_tolerance = 0.5

# time the input has to be held to enter input-repeat mode 
INPUT_HOLD_TO_REPEAT = 1000

# time inbetween each consecutive input when in input-repeat mode
INPUT_REPEAT_DELAY = 500

input_held_event = pygame.event.custom_type()
input_held_repeat_event = pygame.event.custom_type()

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
      elif event.type == input_held_event:
        self.handleInputHeldEvent()
      elif event.type == input_held_repeat_event:
        self.handleInputHeldRepeatEvent()

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
      gamepad.processDirection()
    elif event.type == pygame.JOYHATMOTION:
      gamepad.setDJS(event.hat, event.value)
      gamepad.processDirection()
    elif event.type == pygame.JOYBUTTONDOWN:
      gamepad.setBTN(event.button, 1)
    else:
      # Event type is JOYBUTTONUP
      gamepad.setBTN(event.button, 0)

  def handleInputHeldEvent(self):
    # disable old timer
    pygame.time.set_timer(input_held_event, 0)
    
    held_gamepad = None
    # Find first controller with input_held_mode active and check if the input is still held
    for gamepad in self.gamepads:
      if gamepad.input_held:
        held_gamepad = gamepad
        break
    
    if held_gamepad != None:
      # Start the timer for input held repeat mode
      pygame.time.set_timer(input_held_repeat_event, INPUT_REPEAT_DELAY)
  
  def handleInputHeldRepeatEvent(self):
    held_gamepad = None
    # Find first controller with input_held_mode active and check if the input is still held
    for gamepad in self.gamepads:
      if gamepad.input_held:
        held_gamepad = gamepad
        break
    
    if held_gamepad != None:
      # toggle its direction from neutral to held_direction
      if held_gamepad.current_direction == (0, 0):
        held_gamepad.current_direction = held_gamepad.held_direction
      else:
        held_gamepad.current_direction = (0, 0)
    else:
      # no more held direction, quit input repeat delay mode
      pygame.time.set_timer(input_held_repeat_event, 0)

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

    # Prioritizes digital joysticks, but is essentially an OR of the analog and digital joysticks
    #   (shows any 1 or -1 over 0). It is also processed so that inputs are not repeated without
    #   a small delay.
    self.current_direction = (0, 0)

    # are we in input held mode?
    self.input_held = False

    # if we are in input held mode, which way is it held?
    self.held_direction = (0, 0)

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

  def processDirection (self):
    vertical_dir = 0
    horizontal_dir = 0

    # Check analog directions
    for key in self.current_ajs:
      direction = self.current_ajs[key]
      if abs(direction) > 0:
        if key[1] == "V":
          vertical_dir = direction
        else:
          horizontal_dir = direction

    # Check and prioritize digital directions
    for key in self.current_djs:
      direction = self.current_djs[key]
      if abs(direction[0]) > 0:
        horizontal_dir = direction[0]
      else if abs(direction[1] > 0): # we can use `else if` since only 1 direction changes per event
        vertical_dir = direction

    new_direction = (horizontal_dir, vertical_dir)

    # remember, we treat self.current_direction as the previous direction now

    # update current direction and input_held
    if self.input_held:
      # if the new direction is not the held direction, the user stopped holding the input
      if new_direction != self.held_direction:
        self.input_held = False
        self.current_direction = new_direction

      # otherwise, input_held is still true, do nothing (other methods take over from here)
    else if new_direction != (0, 0) && new_direction == self.current_direction:
      self.input_held = True
      pygame.time.set_timer(input_held_event, INPUT_HOLD_TO_REPEAT)
      # since input is held, we start the input-held timer and set the direction to neutral (so
      #   that the user doesn't fly through the menus by accident)
      self.current_direction = (0, 0)
    else:
      self.current_direction = new_direction