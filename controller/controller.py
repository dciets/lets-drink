import pygame
import sys
import threading
import time

class Controller(threading.Thread):
    BUTTON_PRESSED = pygame.USEREVENT + 1
    BUTTON_RELEASED = pygame.USEREVENT + 2

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                self.read()
                time.sleep(0.001)
        except KeyboardInterrupt:
            pygame.quit()
