from controller import *
import sys

class Keyboard(Controller):
    EVENTS = {True: Controller.BUTTON_PRESSED, False: Controller.BUTTON_RELEASED}

    def __init__(self):
        Controller.__init__(self)

        self.toggles = [False, False]

    def read(self):
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit(0)

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit(0)

            if event.key == pygame.K_w:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_PRESSED, index=Controller.BUTTON1))

            if event.key == pygame.K_s:
                self.toggles[0] = not self.toggles[0]
                pygame.event.post(pygame.event.Event(Keyboard.EVENTS[self.toggles[0]], index=Controller.DRINK1))

            if event.key == pygame.K_i:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_PRESSED, index=Controller.BUTTON2))

            if event.key == pygame.K_k:
                self.toggles[1] = not self.toggles[1]
                pygame.event.post(pygame.event.Event(Keyboard.EVENTS[self.toggles[1]], index=Controller.DRINK2))

        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_w:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=Controller.BUTTON1))

            if event.key == pygame.K_i:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=Controller.BUTTON2))
