from .scene import Scene
from ..ui import BG, Logo, GlowImageButton

logoFadeInDuration = 2.0
btnFadeInDuration = 1.0

class TitleScene (Scene):
  def __init__(self):
    super().__init__()
    self.scene_objs.append(BG("background"))

    # set logo to be transparent at first
    self.logo = Logo((188,75), "amiibrOS logo")
    self.logo.setAlpha(0)

    # Start all buttons off as invisible
    self.resumebtn = GlowImageButton((75, 450), "resume button", "resume")
    self.resumebtn.setAlpha(0)
    self.controllerbtn = GlowImageButton((75, 600), "controller button",
                                         "controller")
    self.controllerbtn.setAlpha(0)
    self.settingsbtn = GlowImageButton((75, 750), "settings button", "settings")
    self.settingsbtn.setAlpha(0)

    self.timeTracker = 0.0
    self.logoFadeIn = True
    self.btnFadeIn = False
    # the index of the selected text button (assigned to visible; 0 is top)
    self.selIdx = 0

    self.scene_objs.extend([self.logo, self.resumebtn, self.controllerbtn,
                            self.settingsbtn])

  def checkLogic(self, input_mgr, dt):
    if self.logoFadeIn:
      # fade in logo whenever this scene is loaded
      if self.timeTracker <= logoFadeInDuration:
        self.logo.fadeIn(self.timeTracker, logoFadeInDuration)
        self.timeTracker += dt
      else:
        # end fade in logo
        self.logoFadeIn = False
        self.logo.fadeIn(logoFadeInDuration, logoFadeInDuration)
        # begin fade-in of buttons as soon as the fade in of logo ends and a
        #   configured controller is detected
        if input_mgr.getConfiguredGamepadCount() > 0:
          self.timeTracker = 0
          self.btnFadeIn = True
        else:
          # TODO, show error screen and ask user to configure
          pass
    elif self.btnFadeIn:
      if self.timeTracker <= btnFadeInDuration:
        self.resumebtn.fadeIn(self.timeTracker, btnFadeInDuration)
        self.controllerbtn.fadeIn(self.timeTracker, btnFadeInDuration)
        self.settingsbtn.fadeIn(self.timeTracker, btnFadeInDuration)
        self.timeTracker += dt
      else:
        self.btnFadeIn = False
        self.logo.fadeIn(btnFadeInDuration, btnFadeInDuration)
    else:
      #TODO handle inputs and scene changes
      # If any input UP,
      # deselect current idx
      # Increment idx with loop around
      # select current idx
      pass
