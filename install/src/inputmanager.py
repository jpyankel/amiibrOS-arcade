import pygame
from pathlib import Path

root_path = (Path(__file__).parent.parent).resolve()
data_path = root_path / "data"

class InputManager:
  def __init__(self):
    # Load joystick module
    pygame.joystick.init()

    # TODO Load joystick config files from data/controllers.config

    # If no gamepads found, main.py will ask to plug in controller
    # If gamepads found, but no config, main.py will ask for setup

  def update(self, dt):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.exit() # TODO HANDLE GRACEFULLY

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.exit() # TODO REMOVE
