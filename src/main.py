import pygame
import pygame_gui

pygame.init()

# amiibrOS Arcade uses a LTN170X2-L02 LCD screen; the spec for resolution is
#   1440x900
res = (1440, 900)

win_surf = pygame.display.set_mode(res, pygame.FULLSCREEN)
ui_mgr = pygame_gui.UIManager(res)

# --- UI Elements ---
logo = pygame.image.load("/usr/bin/amiibrOS/resources/fullscreen-logo.png")

bg = pygame.Surface(res)
bg.fill(pygame.Color("#E8E8E8"))
bg.blit(logo, (0, 0))

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

  # --- ---

  # draw changes to screen
  pygame.display.update()
