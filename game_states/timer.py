import pygame
from controller import Controller

class timer:

    #callback define the next state to run
    def __init__(self, game, nb_sec, callback):
        self.game = game
        self.screen = game.screen
        self.callback = callback
        self.font = pygame.font.SysFont('Comic Sans MS', 72)
        self.delay = 1000
        self.current_time = pygame.time.get_ticks()
        self.sec = nb_sec
        self.timer_x = self.screen.get_width() / 2
        self.timer_y = self.screen.get_height() / 3

    #countdown from the nb_sec to zero then run the callback state
    def run(self):
        time_now = pygame.time.get_ticks()
        # "erase" the previous frame
        self.screen.fill(pygame.Color("black"), (self.timer_x - 25, self.timer_y, 50, 50))
        self.draw_timer()
        if time_now - self.current_time >= self.delay:
            self.current_time = pygame.time.get_ticks()
            self.sec -= 1
        
        if self.sec == 0:
            self.game.state = self.callback
        
        #REEEEEEEEEEEEEEEEEEEEEEEE
        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            pass

    def draw_timer(self):
        textsurface = self.font.render(str(self.sec), False, (200,0,0))
        self.screen.blit(textsurface, (self.timer_x - textsurface.get_width() / 2, self.timer_y))