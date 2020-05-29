from .scene import Scene
from ..ui import BG, Logo

logoFadeInDuration = 2.0

class TitleScene (Scene):
  def __init__(self):
    super().__init__()
    self.scene_objs.append(BG())
    self.scene_objs.append(Logo((0,0)))
    # TODO add buttons which are hidden by default
    self.timeTracker = 0.0
    self.fadeIn = True

  def checkLogic(self, input_mgr, dt):
    # fade in logo whenever this scene is loaded
    if self.fadeIn:
      if self.timeTracker <= logoFadeInDuration:
        self.scene_objs[1].fadeIn(self.timeTracker, logoFadeInDuration)
        self.timeTracker += dt
      else:
        self.fadeIn = False
        self.timeTracker = logoFadeInDuration
        self.scene_objs[1].fadeIn(logoFadeInDuration, logoFadeInDuration)

    #TODO handle inputs and scene changes
