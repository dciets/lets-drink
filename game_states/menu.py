from controller import Controller
import pygame
import pygame.gfxdraw
import yaml

class Menu:

    ITEM_FOREGROUND_COLOR = (100, 150, 255)
    ITEM_FOREGROUND_COLOR_SELECTED = (255, 255, 255)

    def __init__(self, game):
        self.game = game
        self.team1 = 0
        self.team2 = 0
        self.teams = yaml.load(open('data/teams.yml').read())
        self.show_arrows = True
        self.delay = 500
        self.current_time = pygame.time.get_ticks()
        self.change_time = self.current_time + self.delay
        

    def run(self):
        self.game.screen.fill((0,0,0))
        self.current_time = pygame.time.get_ticks()


        #draws a rectangle across the screen (team selector)
        w = self.game.screen.get_width()
        h = 50
        x = 0
        y = (self.game.screen.get_height() - h)/2
        pygame.draw.rect(self.game.screen, (255, 255, 255), (x, y, w, h), 1)


        #Prints title "Choose your teams"
        text = 'Choose your team'
        textsurface = self.game.title_font.render(text, True, (200, 0, 0))
        x = (self.game.screen.get_width() - textsurface.get_width())/2
        y = 0
        self.game.screen.blit(textsurface, (x, y))

        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            if evt.type == Controller.BUTTON_PRESSED and evt.index == 0:
                self.team1 = (self.team1 + 1)%len(self.teams)

            if evt.type == Controller.BUTTON_RELEASED and evt.index == 0:
                pass

            if evt.type == Controller.BUTTON_PRESSED and evt.index == 1:
                self.team2 = (self.team2 + 1)%len(self.teams)

            if evt.type == Controller.BUTTON_RELEASED and evt.index == 1:
                pass


        #prints team 1' name
        team_range = map(lambda x: x%len(self.teams), range(self.team1 - 4, self.team1 + 5))
        for i, team in enumerate(team_range):
            team_name = list(self.teams)[team]
            text = '{} - {} pts'.format(team_name, self.teams[team_name])
            color = Menu.ITEM_FOREGROUND_COLOR_SELECTED if team == self.team1 else Menu.ITEM_FOREGROUND_COLOR
            textsurface = self.game.font.render(text, True, color)
            x = 1*self.game.screen.get_width()/4 - textsurface.get_width()/2
            y = self.game.screen.get_height()/2 - (4 - i)*45 - textsurface.get_height()/2
            self.game.screen.blit(textsurface, (x, y))


        #prints team 2's name
        team_range = map(lambda x: x%len(self.teams), range(self.team2 - 4, self.team2 + 5))
        for i, team in enumerate(team_range):
            team_name = list(self.teams)[team]
            text = '{} - {} pts'.format(team_name, self.teams[team_name])
            color = Menu.ITEM_FOREGROUND_COLOR_SELECTED if team == self.team2 else Menu.ITEM_FOREGROUND_COLOR
            textsurface = self.game.font.render(text, True, color)
            x = 3*self.game.screen.get_width()/4 - textsurface.get_width()/2
            y = self.game.screen.get_height()/2 - (4 - i)*45 - textsurface.get_height()/2
            self.game.screen.blit(textsurface, (x, y))


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


        for evt in pygame.event.get(Controller.WEIGHT):
            print evt.value

        for evt in pygame.event.get():
            pass