from controller import Controller
import pygame

from spike_game import game

class Menu:
    def __init__(self, game):
        self.game = game
        self.s1 = False
        self.s2 = False

    def run(self):
        textsurface = self.game.font.render('Some Text', False, (255, 0, 0))

        self.game.screen.fill((0,0,0))

        self.game.screen.blit(textsurface,(200,200))

        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            if evt.type == Controller.BUTTON_PRESSED and evt.index == 0:
                self.s1 = True

            if evt.type == Controller.BUTTON_RELEASED and evt.index == 0:
                self.s1 = False

            if evt.type == Controller.BUTTON_PRESSED and evt.index == 1:
                self.s2 = True

            if evt.type == Controller.BUTTON_RELEASED and evt.index == 1:
                self.s2 = False

        if self.s1:
            pygame.draw.rect(self.game.screen, (0, 0, 255), (50, 50, 50, 50))

        if self.s2:
            pygame.draw.rect(self.game.screen, (0, 255, 0), (150, 50, 50, 50))

        for evt in pygame.event.get(Controller.WEIGHT):
            print evt.value

        for evt in pygame.event.get():
            pass

        if self.s1 and self.s2:
            self.game.state = game.SpikeGame(self.game.screen, self.game.GAME_WIDTH, self.game.GAME_HEIGHT)