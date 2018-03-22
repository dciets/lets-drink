import pygame
from controller import Controller

class rules:

    #callback define the next state to run
    def __init__(self, game, image, callback):
        self.game = game
        self.screen = game.screen
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.callback = callback
        self.font = pygame.font.SysFont('Roboto', 50)
        self.center_x = self.screen.get_width() / 2
        self.center_y = self.screen.get_height() / 2
        self.player1_ready = False
        self.player2_ready = False

    #show text until both player are ready then run the callback state
    def run(self):
        self.draw_image()
        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            if evt.type == Controller.BUTTON_PRESSED and evt.index == 0:
                self.player1_ready = True
            if evt.type == Controller.BUTTON_PRESSED and evt.index == 1:
                self.player2_ready = True
        
        if self.player1_ready and self.player2_ready:
            self.game.set_timer_state(self.callback)
        
        #REEEEEEEEEEEEEEEEEEEEEEEE
        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):
            pass

    def draw_image(self):
        self.screen.blit(self.image, (self.center_x - self.image.get_width()/2, self.center_y - self.image.get_height()/2))