class Scene:
  def __init__(self):
    # list of objects in the scene in the order they are drawn
    # this should be added to in the subclass init
    self.scene_objs = []
  
  def checkLogic(self, input_mgr, dt):
    """ Handles any current inputs.
    Do not call input_mgr.update(), but rather act on its current inputs
    This must be overriden by the subclass
    """
    pass

  def playTransition(self, transitionID, te):
    """ Updates scene drawing variables depending on the transitionID
    This must be overriden by the subclass

    transitionID: An Int describing which transition to play (if there are any)
    te: elapsed time in milliseconds

    Returns: True when finished, False otherwise
    """
    return False

  def draw(self, screen):
    for obj in self.scene_objs:
      obj.draw(screen, (0,0))
