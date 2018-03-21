import pygame
from yaml import load, dump
from pygame.rect import Rect
from game_states import menu
from game_states import timer
from game_states import selfie
from pygame.time import Clock
import sys


class Game:
    FPS = 40

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    BORDER_SIZE = 10
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
        self.title_font = pygame.font.SysFont('Roboto', 65)

        self.init()

    def init(self):
        pass

    def run(self):
        self.running = True
        while self.running:

            self.state.run()

            pygame.display.update()

            self.timer.tick(Game.FPS)

    def end_game(self, players=['None', 'None'], winners=[False, False]):

        winner = players[[i for i,x in enumerate(winners) if x][0]]
        print "the winner is " + winner
        self.update_yaml(winner)

        self.state = selfie.Selfie(self, players, winners)

    def set_timer_state(self, callback):
        self.state = timer.timer(self, 3, callback)

    def update_yaml(self, winner):

        if not winner:
            return

        stream = file('data/teams.yml', 'r')
        teams = load(stream)
        teams[winner] += 1

        stream = file('data/teams.yml', 'w')
        dump(teams, stream)
