from enum import Enum
from drawables import *
import os
from pathlib import Path

BACKGROUND_FADE_IN_DURATION = 2.0
FADE_OUT_DURATION = 1.0
LOGO_FADE_IN_DURATION = 2.0
SCANNER_ICON_FADE_IN_DURATION = 1.0

root_path = (Path(__file__).parent.parent).resolve()
app_path = root_path / "app"

class State(Enum):
    STARTUP = 0
    TITLE_MENU = 1
    TITLE_MENU_SCANIMATION_SUCCESS = 2
    TITLE_MENU_SCANIMATION_FAILURE = 3

class StateEngine:
    def __init__ (self):
        self.state_logic = {
            State.STARTUP : self.startup_logic,
            State.TITLE_MENU : self.title_menu_logic,
            State.TITLE_MENU_SCANIMATION_SUCCESS : self.title_menu_scanimation_success_logic,
            State.TITLE_MENU_SCANIMATION_FAILURE : self.title_menu_scanimation_failure_logic,
        }

        # Initialize various state variables
        self.reset()

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

            self.title_logo = Logo("amiibrOS logo", (188,75))
            # set logo to be transparent at first
            self.title_logo.setAlpha(0)
            draw_mgr.addDrawable(self.title_logo)

            self.scanner_icon = ScannerIcon("scanner icon", (1219,762))
            self.scanner_icon.setAlpha(0)
            draw_mgr.addDrawable(self.scanner_icon)

            self.scan_prompt = ScanPrompt("scan prompt", (1246,434))
            self.scan_prompt.setAlpha(0)
            draw_mgr.addDrawable(self.scan_prompt)

            self.startup_init = True

        # wait until the background has faded in before moving on
        if not self.title_bg.animating:
            # tell title_logo to fade in
            self.title_logo.playFadeIn(LOGO_FADE_IN_DURATION)

            # transition to the next state
            self.state = State.TITLE_MENU

    def title_menu_logic(self, input_mgr, draw_mgr):
        if not (self.title_logo.animating or self.scanner_icon_anim_started):
            self.scanner_icon.playFadeIn(SCANNER_ICON_FADE_IN_DURATION)
            self.scan_prompt.animating = True
            self.scanner_icon_anim_started = True

        # check if user has scanned an NFC figure
        if input_mgr.scan_complete:
            charID = input_mgr.get_scan() # this will set scan_complete to False automatically

            # check if the charID folder can be found
            if app_exists(charID):
                # app folder for charID is found: Play the animation for charID
                # TODO add, then scan_status_icon.play_success(charID)
                self.fadeout_foreground = FadeOutForeground("fadeout foreground")
                draw_mgr.addDrawable(self.fadeout_foreground)
                self.fadeout_foreground.playFadeIn(FADE_OUT_DURATION)
                # transition to a temporary state to block input and prevent repeated animations
                self.state = State.TITLE_MENU_SCANIMATION_SUCCESS
            else:
                # we couldn't find the app folder for charID: Tell user an error occured
                # TODO add, then scan_status_icon.play_error()
                # transition to a temporary state to block input and prevent repeated animations
                self.state = State.TITLE_MENU_SCANIMATION_FAILURE
            
            self.success_char_id = charID
            

    def title_menu_scanimation_success_logic(self, input_mgr, draw_mgr):
        # wait until scan success animation finishes
        if not self.fadeout_foreground.animating:
            self.scan_success = True

        # note, once self.scan_success == True, the logic state won't matter.
        # main.py will take control from here

    def title_menu_scanimation_failure_logic(self, input_mgr, draw_mgr):
        # wait until scan fail animation finishes
        # if not scan_status_icon.animating:
            # return to title menu
            # self.state = State.TITLE_MENU
        self.state = State.TITLE_MENU

    def reset(self):
        # various state variables for different logic states ---
        self.startup_init = False
        self.scan_success = False
        self.success_char_id = None
        self.scanner_icon_anim_started = False
        # ---

        # various drawables we need ---
        self.title_bg = None
        self.title_logo = None
        self.scanner_icon = None
        self.scan_prompt = None
        self.fadeout_foreground = None
        # ---

        self.state = State.STARTUP

    
def app_exists (charID):
    app_folder = app_path/charID
    app_folder_found = os.path.isdir(app_folder)

    if app_folder_found:
        app = app_folder/(charID + ".sh")
        app_found = os.path.isfile(app)

        if app_found:
            return True
    
    return False