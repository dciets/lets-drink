from controller import Controller
import pygame
import pygame.gfxdraw
import yaml
from spike_game import spike_game
from game_states import rules
from bg_menu import Background

class Menu:

    ITEM_FOREGROUND_COLOR = (0, 0, 0)
    ITEM_FOREGROUND_COLOR_SELECTED = (255, 255, 255)

    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.team1 = 0
        self.team2 = 0
        self.teams = yaml.load(open('data/teams.yml').read())
        self.show_arrows = True
        self.delay = 500
        self.current_time = pygame.time.get_ticks()
        self.change_time = self.current_time + self.delay
        self.ready = [False, False]
        self.background = Background(game)

    def run(self):
        self.background.draw()
        self.current_time = pygame.time.get_ticks()


        #draws a rectangle across the screen (team selector)
        w = self.game.screen.get_width()
        h = 50
        x = 0
        y = (self.game.screen.get_height() - h)/2
        pygame.draw.rect(self.game.screen, (255, 255, 255), (x, y, w, h), 1)


        #Prints title "Choose your teams"
        text = 'Choose your team'
        textsurface = self.game.title_font.render(text, True, (255,255,0))
        textsurface2 = self.game.title_font.render(text, True, (0,0,0))        
        x = (self.game.screen.get_width() - textsurface.get_width())/2
        y = 0

        for dx in [-1, 0, 1]:
                for dy in [-2, 0, 2]:
                    self.game.screen.blit(textsurface2, (x + dx, y + dy))
        self.game.screen.blit(textsurface, (x, y))

        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            if evt.type == Controller.BUTTON_PRESSED and evt.index == Controller.BUTTON1:
                if not self.ready[0]:
                    self.team1 = (self.team1 + 1) % len(self.teams)

            if evt.type == Controller.BUTTON_PRESSED and evt.index == Controller.BUTTON2:
                if not self.ready[1]:
                    self.team2 = (self.team2 + 1) % len(self.teams)

            if evt.type == Controller.BUTTON_PRESSED:
                if evt.index == Controller.DRINK1:
                    self.ready[0] = True

                if evt.index == Controller.DRINK2:
                    self.ready[1] = True

            if evt.type == Controller.BUTTON_RELEASED:
                if evt.index == Controller.DRINK1:
                    self.ready[0] = False
                    self.couting = False

                if evt.index == Controller.DRINK2:
                    self.ready[1] = False
                    self.couting = False


        #prints team 1' name
        team_range = map(lambda x: x%len(self.teams), range(self.team1 - 4, self.team1 + 5))
        for i, team in enumerate(team_range):
            team_name = list(self.teams)[team]
            text = '{} - {} pts'.format(team_name, self.teams[team_name])
            color = Menu.ITEM_FOREGROUND_COLOR_SELECTED if team == self.team1 else Menu.ITEM_FOREGROUND_COLOR
            bg_color = (0,0,0) if team == self.team1 else (255,255,255)
            textsurface = self.game.font.render(text, True, color)
            textsurface2 = self.game.font.render(text, True, bg_color)
            x = 1*self.game.screen.get_width()/4 - textsurface.get_width()/2
            y = self.game.screen.get_height()/2 - (4 - i)*45 - textsurface.get_height()/2
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    self.game.screen.blit(textsurface2, (x + dx, y + dy))
            self.game.screen.blit(textsurface, (x, y))

        if self.ready[0]:
            ts1 = self.game.title_font.render("READY", True, (0, 255, 0))
            ts2 = self.game.title_font.render("READY", True, (0, 0, 0))
            x, y = (self.game.screen.get_width() / 4 - ts1.get_width()/2, self.game.screen.get_height() / 2 - ts1.get_height()/2)
            for dx in [-5, 0, 5]:
                for dy in [-5, 0, 5]:
                    self.game.screen.blit(ts2, (x + dx, y + dy))
            self.game.screen.blit(ts1, (x, y))


        #prints team 2's name
        team_range = map(lambda x: x%len(self.teams), range(self.team2 - 4, self.team2 + 5))
        for i, team in enumerate(team_range):
            team_name = list(self.teams)[team]
            text = '{} - {} pts'.format(team_name, self.teams[team_name])
            color = Menu.ITEM_FOREGROUND_COLOR_SELECTED if team == self.team2 else Menu.ITEM_FOREGROUND_COLOR
            bg_color = (0,0,0) if team == self.team2 else (255,255,255)
            textsurface = self.game.font.render(text, True, color)
            textsurface2 = self.game.font.render(text, True, bg_color)
            x = 3*self.game.screen.get_width()/4 - textsurface.get_width()/2
            y = self.game.screen.get_height()/2 - (4 - i)*45 - textsurface.get_height()/2
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    self.game.screen.blit(textsurface2, (x + dx, y + dy))
            self.game.screen.blit(textsurface, (x, y))

        if self.ready[1]:
            ts1 = self.game.title_font.render("READY", True, (0, 255, 0))
            ts2 = self.game.title_font.render("READY", True, (0, 0, 0))
            x, y = (3*self.game.screen.get_width() / 4 - ts1.get_width()/2, self.game.screen.get_height() / 2 - ts1.get_height()/2)
            for dx in [-5, 0, 5]:
                for dy in [-5, 0, 5]:
                    self.game.screen.blit(ts2, (x + dx, y + dy))
            self.game.screen.blit(ts1, (x, y))

        #draws the flashing arrows
        if self.current_time >= self.change_time:
            self.change_time = self.current_time + self.delay
            self.show_arrows = not self.show_arrows

        if self.show_arrows:
            w = 50
            h = 15
            x = 1*self.game.screen.get_width()/4 - w/2
            y = self.game.screen.get_height() - h
            pygame.gfxdraw.filled_polygon(self.game.screen, [(x, y), (x + w, y), (x + w/2, y + h)], (255, 255, 255))
            pygame.gfxdraw.aapolygon(self.game.screen, [(x, y), (x + w, y), (x + w/2, y + h)], (255, 255, 255))

            x = 3*self.game.screen.get_width()/4 - w/2
            pygame.gfxdraw.filled_polygon(self.game.screen, [(x, y), (x + w, y), (x + w/2, y + h)], (255, 255, 255))
            pygame.gfxdraw.aapolygon(self.game.screen, [(x, y), (x + w, y), (x + w/2, y + h)], (255, 255, 255))


        for evt in pygame.event.get():
            pass

        if all(self.ready):

            spikegame = spike_game.SpikeGame(self.game, (self.teams.keys()[self.team1], self.teams.keys()[self.team2]))
            #TODO nice rule message
            self.game.state = rules.rules(self.game, "sprites/rule1.png", spikegame)
