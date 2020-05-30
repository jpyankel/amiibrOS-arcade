from .scene import Scene
from ..ui import BG, Logo, ImageButton

logoFadeInDuration = 2.0

class TitleScene (Scene):
  def __init__(self):
    super().__init__()
    self.scene_objs.append(BG("background"))

    # set logo to be transparent at first
    logo = Logo((188,75), "amiibrOS logo")
    logo.setAlpha(0)
    self.scene_objs.append(logo)

    # TODO add buttons which are hidden by default
    self.timeTracker = 0.0
    self.fadeIn = True

    resumebtn = ImageButton((75, 450), "resume button", "resume")
    controllerbtn = ImageButton((75, 600), "controller button", "controller")
    settingsbtn = ImageButton((75, 750), "settings button", "settings")
    self.scene_objs.extend([resumebtn, controllerbtn, settingsbtn])

  def checkLogic(self, input_mgr, dt):
    # fade in logo whenever this scene is loaded
    if self.fadeIn:
      # TODO Change this to refer to local variable logo instead of array indexing. waste of cycles
      if self.timeTracker <= logoFadeInDuration:
        self.scene_objs[1].fadeIn(self.timeTracker, logoFadeInDuration)
        self.timeTracker += dt
      else:
        self.fadeIn = False
        self.timeTracker = logoFadeInDuration
        self.scene_objs[1].fadeIn(logoFadeInDuration, logoFadeInDuration)

    #TODO handle inputs and scene changes
