import pygame
import sys
import threading

class Controller(threading.Thread):
    BUTTON_PRESSED = pygame.USEREVENT + 1
    BUTTON_RELEASED = pygame.USEREVENT + 2
    WEIGHT = pygame.USEREVENT + 3

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                self.read()
        except KeyboardInterrupt:
            pygame.quit()
