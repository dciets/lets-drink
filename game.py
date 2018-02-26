import pygame
from pygame.rect import Rect
from game_states import menu
from pygame.time import Clock
import sys


class Game:
    FPS = 30

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BORDER_SIZE = 25
    GAME_WIDTH = SCREEN_WIDTH - 2 * BORDER_SIZE
    GAME_HEIGHT = SCREEN_HEIGHT - 2 * BORDER_SIZE
    GAME_TOP = BORDER_SIZE
    GAME_BOTTOM = SCREEN_HEIGHT - BORDER_SIZE
    GAME_LEFT = BORDER_SIZE
    GAME_RIGHT = SCREEN_HEIGHT - BORDER_SIZE

    def __init__(self, border):
        '''Init game state, player score, game count, etc...'''
        self.border = border
        self.state = menu.Menu(self)
        self.screen = border.subsurface(Rect((Game.BORDER_SIZE, Game.BORDER_SIZE), (Game.SCREEN_WIDTH - 2 * Game.BORDER_SIZE, Game.SCREEN_HEIGHT - 2 * Game.BORDER_SIZE)))
        self.timer = Clock()

        self.font = pygame.font.SysFont('Roboto', 30)

        self.init()

    def init(self):
        pass

    def run(self):
        self.running = True
        while self.running:

            self.state.run()

            pygame.display.update()

            self.timer.tick(Game.FPS)