#!/usr/bin/env python2
import pygame
import game
import os
import controller
from threading import Thread
import sys
import pygame.camera


ON_ARCADE = os.getlogin() == 'capra'

def main():
    pygame.init()
    pygame.display.set_caption("L'ETS be sobre")

    pygame.camera.init()
    pygame.font.init()

    if ON_ARCADE:
        ctrl = controller.USB()
        border = pygame.display.set_mode((game.Game.SCREEN_WIDTH, game.Game.SCREEN_HEIGHT), pygame.FULLSCREEN) #, pygame.FULLSCREEN)
    else:
        ctrl = controller.Keyboard()
        border = pygame.display.set_mode((game.Game.SCREEN_WIDTH, game.Game.SCREEN_HEIGHT))

    ctrl.start()

    try:
        while True:
            app = game.Game(border)

            print("Start game")
            app.run()
            print("Game stop")
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
