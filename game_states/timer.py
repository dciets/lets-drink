import pygame
from controller import Controller

class timer:

    #callback define the next state to run
    def __init__(self, game, nb_sec, callback):
        self.game = game
        self.screen = game.screen
        self.callback = callback
        self.font = pygame.font.SysFont('Roboto', 72)
        self.delay = 1000
        self.current_time = pygame.time.get_ticks()
        self.sec = nb_sec
        self.timer_x = self.screen.get_width() / 2
        self.timer_y = self.screen.get_height() / 3

    #countdown from the nb_sec to zero then run the callback state
    def run(self):
        time_now = pygame.time.get_ticks()
        
        #if your callback have a draw function will be use to "clean" the screen on each frame
        #else the timer "clean" himself by drawing a black box over himself 
        try:
            self.callback.draw()
        except AttributeError:
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
        x = self.timer_x - textsurface.get_width() / 2
        y = self.timer_y
        self.draw_outline(x, y, str(self.sec), (255,255,255), 1)
        self.screen.blit(textsurface, (x, y))

    def draw_outline(self, x, y, text, color, offset):
        textsurface2 = self.font.render(text, False, color)
        for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    self.game.screen.blit(textsurface2, (x + dx, y + dy))