import pygame
from input_manager import InputManager
from state_engine import StateEngine
from draw_manager import DrawManager

# configurations
DRAW_FPS_OVERLAY = True

if __name__ == "__main__":
    # initialization step
    pygame.init()
    input_mgr = InputManager()
    state_eng = StateEngine()
    draw_mgr = DrawManager()
    clock = pygame.time.Clock()

    while not input_mgr.keyboard_forcequit:
        # limit frontend graphics and logic to roughly 60 Hz
        dt = clock.tick(60)/1000.0

        # --- Main Loop ---
        # update inputs, this will automatically set flags we need to check for main logic
        input_mgr.update(dt)

        # now do main logic depending on state
        state_eng.update(input_mgr, draw_mgr)

        # now draw updated scene objects to the screen
        draw_mgr.update(dt, clock.get_fps() if DRAW_FPS_OVERLAY else None)

        # -----------------