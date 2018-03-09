import player
from spike import spike
from shapely.geometry import Polygon
import pygame
import math
import time
import threading
from random import randint
from controller import Controller


##TODO: use de delta t for the redraw
class SpikeGame:

    background_color = (0, 0 ,0)
    start = 0
    font = ""
    clock = 0
    round_end = False
    screen = ""

    getTicksLastFrame = 0
    dt = 0.01

    spike_color = (125, 125, 125, 0)
    spike_width = 0
    spike_height = 0

    PLAYER_VELX = 400

    PLAYER1_SPRITE = "sprites/spaceship1.png"
    PLAYER2_SPRITE = "sprites/spaceship2.png"
    #spike position in screen
    SPIKE_POSITION = ["TOP", "BOTTOM", "LEFT", "RIGHT"]

    spike_arr = []
    static_spike_arr = []
    level = 1

    STOCK = 3
    players_stock = [STOCK, STOCK]

    WIDTH_MAGIC_NUMBER = 0.0546875
    HEIGHT_MAGIC_NUMBER = 0.064814815
    JUMP_SPEED_MAGIC_NUMBER = 1.851851852

    screen_size = (0, 0)

    def __init__(self, game, players_name):

        self.screen = game.screen
        self.start = time.time()
        self.font = pygame.font.SysFont('Comic Sans MS', 72)
        self.clock = pygame.time.Clock()
        self.screen_size = [self.screen.get_width(), self.screen.get_height()]
        self.players_name = players_name
        self.spike_width = self.screen_size[0] / 15
        self.spike_height = self.screen_size[1] / 15
        self.player1, self.player2 = self.create_players()
        self.gen_static_spike()

    def create_players(self):

        #ajusting value with sreen ratio
        w = int(self.WIDTH_MAGIC_NUMBER * self.screen_size[0])
        h = int(self.HEIGHT_MAGIC_NUMBER * self.screen_size[1])
        jump_speed = -1 * self.screen_size[1] * self.JUMP_SPEED_MAGIC_NUMBER

        ship1 = pygame.image.load(self.PLAYER1_SPRITE).convert_alpha()
        ship1 = pygame.transform.scale(ship1, (w, h))
        player1 = player.player(w, h, (0, 100), self.PLAYER_VELX, ship1, self.players_name[0])
        player1.jump_speed = jump_speed

        ship2 = pygame.image.load(self.PLAYER2_SPRITE).convert_alpha()
        ship2 = pygame.transform.scale(ship2, (w, h))
        ship2 = pygame.transform.flip(ship2, True, False)  # flip image
        start2 = (self.screen_size[0] - player1.width, 100)
        player2 = player.player(w, h, start2, -self.PLAYER_VELX, ship2, self.players_name[1])
        player2.jump_speed = jump_speed

        return player1, player2

    def run(self):

        #getting nb tick since last run call
        t = pygame.time.get_ticks()
        #dt since last tick
        self.dt = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t

        self.screen.fill(self.background_color)
        self.draw_spikes()
        self.draw_level()
        self.draw_stock()
        self.draw_end_round()
            
        #custom event for the arcade controller (Press W and I on a keyboard)
        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            if  evt.type == Controller.BUTTON_PRESSED and evt.index == 0:
                self.player1.jump()

            if  evt.type == Controller.BUTTON_PRESSED and evt.index == 1:
                self.player2.jump()

        self.is_player_alive()

        if self.player1.is_alive and self.player2.is_alive:
            self.update_player(self.player1)
            self.update_player(self.player2)

        # check if players touch the edges (both touch at the same time)
        if self.player1.x < 0 or self.player1.x > self.screen_size[0] - self.player1.width:
            if self.player1.is_alive or self.player2.is_alive:
                d = threading.Thread(name='gen_spike', target=self.gen_spikes)
                d.start()
                self.level += 1

        # render our cute image
        self.screen.blit(self.player1.image, self.player1.get_position())
        self.screen.blit(self.player2.image, self.player2.get_position())

        pygame.display.flip()

    def update_player(self, player):
        player.update_y_velocity(0.01)
        player.update_y_position(0.01)
        #redraw player x position relative to the dt
        player.update_x_position(self.screen_size[0], self.dt)

    def draw_level(self):
        level_txt = self.font.render(str(self.level), False, (0, 255, 0))
        self.screen.blit(level_txt, ((self.screen_size[0] / 2 ) - (level_txt.get_width()/2), 50))

    def draw_spikes(self):
        for spike in self.spike_arr + self.static_spike_arr:
            if spike.position == self.SPIKE_POSITION[0]:
                self.screen.blit(spike.get_spike_image(self.spike_color), (spike.get_x(), spike.get_y()))
            elif spike.position == self.SPIKE_POSITION[1]:
                self.screen.blit(pygame.transform.flip(spike.get_spike_image(self.spike_color), False, True), (spike.get_x(), spike.get_y() - spike.height))
            elif spike.position == self.SPIKE_POSITION[2]:
                self.screen.blit(pygame.transform.rotate(spike.get_spike_image(self.spike_color), 90), (spike.get_x(), spike.get_y()))
            elif spike.position == self.SPIKE_POSITION[3]:
                self.screen.blit(pygame.transform.rotate(spike.get_spike_image(self.spike_color), 270), (spike.get_x() - spike.height, spike.get_y()))
            #pygame.draw.polygon(self.screen, self.spike_color, spike.polygone)

    def gen_static_spike(self):
        width = self.screen_size[0]
        height = self.screen_size[1]

        for i in xrange(1, width, self.spike_width):
            p = [(i,0),(i + self.spike_width/2, self.spike_height),(i + self.spike_width, 0)]
            self.static_spike_arr.append(spike(self.spike_width, self.spike_height, p, self.SPIKE_POSITION[0]))
            p = [(i,height),(i + self.spike_width/2, height - self.spike_height),(i + self.spike_width, height)]
            self.static_spike_arr.append(spike(self.spike_width, self.spike_height, p, self.SPIKE_POSITION[1]))

    def gen_spikes(self):
        time.sleep(0.5)
        if self.player1.is_alive or self.player2.is_alive:
            w = self.screen_size[0]
            h = self.screen_size[1]

            self.random_spike_color()

            max_val = (self.screen_size[1] / self.spike_width) - 3
            r = randint(min((self.level / 2), max_val - 4), max_val)
            self.spike_arr = []

            while len(self.spike_arr) < r :
                b = randint(1, max_val) * self.spike_width
                while b in self.spike_arr:
                    b = randint(1, max_val + 1) * self.spike_width
                
                p = [(0,b),(self.spike_height, b + self.spike_width/2),(0,b + self.spike_width)]
                self.spike_arr.append(spike(self.spike_width, self.spike_height, p, self.SPIKE_POSITION[2]))
                p = [(w,b),(w - self.spike_height, b + self.spike_width/2),(w,b + self.spike_width)]
                self.spike_arr.append(spike(self.spike_width, self.spike_height, p, self.SPIKE_POSITION[3]))

    def random_spike_color(self):
        r = randint(125, 175)
        g = randint(125, 175)
        b = randint(125, 175)
        self.spike_color = (r, g, b, 0)

    def game_reset(self):
        self.player1, self.player2 = self.create_players()

        self.level = 1
        self.spike_arr = []
        self.static_spike_arr = []
        self.gen_static_spike()
        if any(x == 0 for x in self.players_stock):
            self.players_stock = [self.STOCK, self.STOCK]

    def is_player_alive(self):
        p1 = Polygon(self.player1.get_polygon())
        p2 = Polygon(self.player2.get_polygon())

        for spike in self.static_spike_arr + self.spike_arr:
            s = Polygon(spike.polygone)
            if p1.intersects(s):
                self.player1.is_alive = False
            if p2.intersects(s):
                self.player2.is_alive = False

        if not (self.player1.is_alive and self.player2.is_alive) and not self.round_end:
            self.remove_stock()
        
        if(any(x == 0 for x in self.players_stock)):
            self.draw_end_game_msg()

    def remove_stock(self):
        if not self.round_end:
            if not self.player1.is_alive:
                self.players_stock[0] = self.players_stock[0] - 1
        
            if not self.player2.is_alive:
                self.players_stock[1] = self.players_stock[1] - 1
            
            self.round_end = True
            self.wait_for_next_round()

    def wait_for_next_round(self):
        cnt = (not self.player1.is_alive) + (not self.player2.is_alive)
        a = 0
        b = 0
        while self.round_end:
            self.draw_stock()
            self.run()
            for evt in pygame.event.get([Controller.WEIGHT]):
                if evt.type == Controller.WEIGHT and evt.index == 0 and not self.player1.is_alive:
                    a = 1
                if evt.type == Controller.WEIGHT and evt.index == 1 and not self.player2.is_alive:
                    b = 1
            
            if cnt - a - b == 0:
                self.round_end = False
                self.game_reset()
    
    def draw_end_round(self):
        if not (self.player1.is_alive or self.players_stock[0] == 0):
            textsurface = self.font.render(self.player1.name + ' lost one life!', False, (255, 0, 0))
            self.screen.blit(textsurface,((self.screen_size[0] / 2 ) - (textsurface.get_width()/2),
                (self.screen_size[1] / 2) - (textsurface.get_height()/2)-35))
        if not (self.player2.is_alive or self.players_stock[1] == 0):
            textsurface = self.font.render(self.player2.name + ' lost one life!', False, (255, 0, 0))
            self.screen.blit(textsurface,((self.screen_size[0] / 2 ) - (textsurface.get_width()/2),
                (self.screen_size[1] / 2) - (textsurface.get_height()/2)+35))

    def draw_end_game_msg(self):
        if self.players_stock[0] == 0:
            textsurface = self.font.render(self.player1.name + ' lost the game!', False, (255, 0, 0))
            self.screen.blit(textsurface,((self.screen_size[0] / 2 ) - (textsurface.get_width()/2),
                (self.screen_size[1] / 2) - (textsurface.get_height()/2)-35))
        if self.players_stock[1] == 0:
            textsurface = self.font.render(self.player2.name + ' lost the game!', False, (255, 0, 0))
            self.screen.blit(textsurface,((self.screen_size[0] / 2 ) - (textsurface.get_width()/2),
                (self.screen_size[1] / 2) - (textsurface.get_height()/2)+35))

    def draw_stock(self):
        for x in xrange(self.STOCK):
            #player 2
            pygame.draw.circle(self.screen, (0,0,255), (self.screen_size[0]/2 + (x + 1) * 20, self.spike_height + 10), 5)
            if x >= self.players_stock[1]:
                pygame.draw.line(self.screen, (255, 0, 0), (self.screen_size[0]/2 + (x + 1) * 20 - 3, self.spike_height + 7),
                    (self.screen_size[0]/2 + (x + 1) * 20 + 3, self.spike_height + 13), 2)
                pygame.draw.line(self.screen, (255, 0, 0), (self.screen_size[0]/2 + (x + 1) * 20 + 3, self.spike_height + 7),
                    (self.screen_size[0]/2 + (x + 1) * 20 - 3, self.spike_height + 13), 2)
            
            #player 1
            pygame.draw.circle(self.screen, (0,0,255), (self.screen_size[0]/2 - (x + 1) * 20, self.spike_height + 10), 5)
            if x >= self.players_stock[0]:
                pygame.draw.line(self.screen, (255, 0, 0), (self.screen_size[0]/2 - (x + 1) * 20 - 3, self.spike_height + 7),
                    (self.screen_size[0]/2 - (x + 1) * 20 + 3, self.spike_height + 13), 2)
                pygame.draw.line(self.screen, (255, 0, 0), (self.screen_size[0]/2 - (x + 1) * 20 + 3, self.spike_height + 7),
                    (self.screen_size[0]/2 - (x + 1) * 20 - 3, self.spike_height + 13), 2)