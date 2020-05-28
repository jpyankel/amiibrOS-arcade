import pygame
import pygame_gui
import pygame.joystick

pygame.init()
pygame.joystick.init()

# --- Taken code from docs ---
BLACK = pygame.Color('black')
# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
  def __init__(self):
    self.reset()
    self.font = pygame.font.Font(None, 20)

  def tprint(self, win_surf, textString):
    textBitmap = self.font.render(textString, True, BLACK)
    win_surf.blit(textBitmap, (self.x, self.y))
    self.y += self.line_height

  def reset(self):
    self.x = 10
    self.y = 10
    self.line_height = 15

  def indent(self):
    self.x += 10

  def unindent(self):
    self.x -= 10

textPrint = TextPrint()

# --- Taken code from docs ---

# amiibrOS Arcade uses a LTN170X2-L02 LCD screen; the spec for resolution is
#   1440x900
res = (1440, 900)

win_surf = pygame.display.set_mode(res, pygame.FULLSCREEN)
ui_mgr = pygame_gui.UIManager(res)

# --- UI Elements ---
#logo = pygame.image.load("/usr/bin/amiibrOS/resources/fullscreen-logo.png")

bg = pygame.Surface(res)
bg.fill(pygame.Color("#E8E8E8"))
#bg.blit(logo, (0, 0))

hello_button = pygame_gui.elements.UIButton(
  relative_rect=pygame.Rect((350, 275), (100, 50)),
  text="Say Hello",
  manager=ui_mgr)
# --- ---

clock = pygame.time.Clock()
is_running = True

while is_running:
  dt = clock.tick(60)/1000.0 # limit frontend graphics to roughly 60 FPS

  # --- Event Handler ---
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      is_running = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        is_running = False

    if event.type == pygame.USEREVENT:
      if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == hello_button:
            print("Hello World!")

    ui_mgr.process_events(event)

  # --- ---

  # update UI state
  ui_mgr.update(dt)

  # --- Draw loop ---
  win_surf.blit(bg, (0, 0))
  ui_mgr.draw_ui(win_surf)

  # --- More taken code ---
  textPrint.reset()

  # Get count of joysticks.
  joystick_count = pygame.joystick.get_count()
  textPrint.tprint(win_surf, "Number of joysticks: {}".format(joystick_count))
  textPrint.indent()
  # For each joystick:
  for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

    textPrint.tprint(win_surf, "Joystick {}".format(i))
    textPrint.indent()

    # Get the name from the OS for the controller/joystick.
    name = joystick.get_name()
    textPrint.tprint(win_surf, "Joystick name: {}".format(name))

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    textPrint.tprint(win_surf, "Number of axes: {}".format(axes))
    textPrint.indent()

    for i in range(axes):
      axis = joystick.get_axis(i)
      textPrint.tprint(win_surf, "Axis {} value: {:>6.3f}".format(i, axis))
    textPrint.unindent()

    buttons = joystick.get_numbuttons()
    textPrint.tprint(win_surf, "Number of buttons: {}".format(buttons))
    textPrint.indent()

    for i in range(buttons):
      button = joystick.get_button(i)
      textPrint.tprint(win_surf,
                       "Button {:>2} value: {}".format(i, button))
    textPrint.unindent()

    hats = joystick.get_numhats()
    textPrint.tprint(win_surf, "Number of hats: {}".format(hats))
    textPrint.indent()

    # Hat position. All or nothing for direction, not a float like
    # get_axis(). Position is a tuple of int values (x, y).
    for i in range(hats):
      hat = joystick.get_hat(i)
      textPrint.tprint(win_surf, "Hat {} value: {}".format(i, str(hat)))
    textPrint.unindent()
    textPrint.unindent()
  # --- End Taken Code ---
  # --- ---

  # draw changes to screen
  pygame.display.update()
