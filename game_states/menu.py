from controller import Controller
import pygame

from spike_game import game

class Menu:
    def __init__(self, game):
        self.game = game

        self.buttons = [False] * 4

    def run(self):
        textsurface = self.game.font.render('Some Text', False, (255, 0, 0))

        self.game.screen.fill((0,0,0))

        self.game.screen.blit(textsurface,(200,200))

        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            if evt.type == Controller.BUTTON_PRESSED:
                self.buttons[evt.index] = True

            if evt.type == Controller.BUTTON_RELEASED:
                self.buttons[evt.index] = False


        for i in range(len(self.buttons)):
            if self.buttons[i]:
                pygame.draw.rect(self.game.screen, (0, 0, 255), (50 + i * 50, 50, 50, 50))

        for evt in pygame.event.get():
            pass

        if self.s1 and self.s2:
            players_name = ("ETS", "ULaval")
            self.game.state = game.SpikeGame(self.game, players_name)