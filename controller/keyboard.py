from controller import *
import sys

class Keyboard(Controller):
    def __init__(self):
        self.weight_flags = [False, False]
        self.weight_value = [750, 750]

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

            if event.key == pygame.K_s and not self.weight_flags[0]:
                self.weight_flags[0] = True
                self.weight_value[0] -= 50

                pygame.event.post(pygame.event.Event(Controller.WEIGHT, index=0, value=0))

            if event.key == pygame.K_i:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_PRESSED, index=1))

            if event.key == pygame.K_k and not self.weight_flags[1]:
                self.weight_flags[1] = True
                self.weight_value[1] -= 50

                pygame.event.post(pygame.event.Event(Controller.WEIGHT, index=1, value=0))

        if self.weight_flags[0]:
            self.weight_flags[0] = False
            pygame.event.post(pygame.event.Event(Controller.WEIGHT, index=0, value=self.weight_value[0]))

        if self.weight_flags[1]:
            self.weight_flags[1] = False
            pygame.event.post(pygame.event.Event(Controller.WEIGHT, index=1, value=self.weight_value[1]))

        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_w:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=0))

            if event.key == pygame.K_i:
                pygame.event.post(pygame.event.Event(Controller.BUTTON_RELEASED, index=1))
