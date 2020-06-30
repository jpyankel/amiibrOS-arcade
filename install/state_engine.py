from enum import Enum
from drawables import *

BACKGROUND_FADE_IN_DURATION = 2.0
LOGO_FADE_IN_DURATION = 2.0
#BTN_FADE_IN_DURATION = 1.0

class State(Enum):
    STARTUP = 0
    TITLE_MENU = 1

class StateEngine:
    def __init__ (self):
        self.state = State.STARTUP

        self.state_logic = {
            State.STARTUP : self.startup_logic,
            State.TITLE_MENU : self.title_menu_logic
        }

        # various state variables for different logic states ---
        self.startup_init = False
        # ---

        # various drawables we need ---
        self.title_bg = None
        self.title_logo = None
        # ---

    def update(self, input_mgr, draw_mgr):
        # depending on our state, we branch to a different function
        self.state_logic[self.state](input_mgr, draw_mgr)

    def startup_logic(self, input_mgr, draw_mgr):
        if not self.startup_init:
            # initialize all drawables
            self.title_bg = Background("blank_background")
            # tell background to fade from black to white
            self.title_bg.playFadeBlackWhite(BACKGROUND_FADE_IN_DURATION)
            draw_mgr.addDrawable(self.title_bg)

            self.title_logo = Logo((188,75), "amiibrOS logo")
            # set logo to be transparent at first
            self.title_logo.setAlpha(0)
            draw_mgr.addDrawable(self.title_logo)

            self.startup_init = True

        # wait until the background has faded in before moving on
        if not self.title_bg.animating:
            self.state = State.TITLE_MENU

    def title_menu_logic(self, input_mgr, draw_mgr):
        # TODO LOGIC
        #self.title_logo.playFadeIn(LOGO_FADE_IN_DURATION)
        pass