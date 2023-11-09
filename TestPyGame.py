import os
import pygame
import time

def FindDisplayDriver():
  for driver in ["fbcon", "directfb", "svgalib"]:
    if not os.getenv("SDL_VIDEODRIVER"):
      os.putenv("SDL_VIDEODRIVER", driver)
    try:
      pygame.display.init()
      return True
    except pygame.error:
      pass
  return False

if __name__ == "__main__":
  os.environ["SDL_FBDEV"] = "/dev/fb0"
  pygame.init()
  if not FindDisplayDriver():
    print("Failed to initialise display driver")
  else:
    pygame.mouse.set_visible(False)
    width  = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    screen.fill((0x3F, 0, 0))
    pygame.display.update()
    print(pygame.display.Info())
    time.sleep(5)
    pygame.quit()