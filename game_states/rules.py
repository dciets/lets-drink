import pygame
from controller import Controller

class rules:

    #callback define the next state to run
    def __init__(self, game, text, callback):
        self.game = game
        self.screen = game.screen
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont('Comic Sans MS', 50)
        self.text_x = self.screen.get_width() / 2
        self.text_y = self.screen.get_height() / 2
        self.player1_ready = False
        self.player2_ready = False

    #show text until both player are ready then run the callback state
    def run(self):
        self.draw_rules()
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

    def draw_rules(self):
        textsurface = self.font.render(str(self.text), False, (0,255,128))
        self.screen.blit(textsurface, (self.text_x - textsurface.get_width()/2, self.text_y))