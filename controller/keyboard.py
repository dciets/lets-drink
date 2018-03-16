from controller import *
import sys

class Keyboard(Controller):
    def __init__(self):

        Controller.__init__(self)

    def read(self):
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit(0)

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit(0)

            if event.key == pygame.K_w:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_PRESSED, index=0))

            if event.key == pygame.K_s:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_PRESSED, index=2))

            if event.key == pygame.K_i:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_PRESSED, index=1))

            if event.key == pygame.K_k:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_PRESSED, index=3))

        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_w:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=0))

            if event.key == pygame.K_s:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=2))

            if event.key == pygame.K_i:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=1))

            if event.key == pygame.K_k:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=3))
