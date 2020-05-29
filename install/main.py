import pygame
from src.scenemanager import SceneManager
from src.scene import TitleScene

# TODO
# blank -> title
# title -(noctlr)> nocontroller
# title -(unconfigctrl)> unconfiguredcontroller
# title -(animcomplete)> main
# main -(noinput10s)> slideshow
# the logic must check for drawTransition's return value (0 if incomplete, 1 if complete)

if __name__ == "__main__":
  # initialize step
  pygame.init()
  scene_mgr = SceneManager()
  clock = pygame.time.Clock()

  # load first scene
  initial_scene = TitleScene()
  scene_mgr.loadScene(initial_scene)

  while True:
    # limit frontend graphics and logic to roughly 60 Hz
    dt = clock.tick(60)/1000.0 

    # --- Main Loop ---

    # do scene specific logic (also depends on input)
    # then draw the result to the screen
    scene_mgr.update(dt)

    # -----------------
