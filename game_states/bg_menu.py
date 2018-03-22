import pygame

class Background:

    STATIC_BG = "sprites/bg.png"
    STATIC_BG2 = "sprites/bg2.png"
    LETS_PLAY_BG = "sprites/logo.png"
    INIT_DELAY = 20
    MAX_SCALE = 200

    def __init__(self, game):
        self.screen = game.screen
        self.angle = 0
        self.scale = 5
        self.time = pygame.time.get_ticks()
        self.time2 = pygame.time.get_ticks()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.static_bg = pygame.image.load(self.STATIC_BG)
        self.static_bg = pygame.transform.scale(self.static_bg, (self.width, self.height))
        self.static_rect = self.static_bg.get_rect()
        self.letsplay_bg = pygame.image.load(self.LETS_PLAY_BG)
        self.original_letsplay = pygame.image.load(self.LETS_PLAY_BG)
        self.delay = 50
        self.scale_image = False
        self.is_zooming = True
        self.init_bg = True
    
    def draw(self):
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.static_bg, self.static_rect)
        self.screen.blit(self.letsplay_bg, self.lets_play_image_coord())
        time_now = pygame.time.get_ticks()
        if time_now - self.time >= self.delay:
            self.zoom_image = False
            self.delay = self.INIT_DELAY
            self.time = pygame.time.get_ticks()
            self.rotate()
            self.is_zooming = True
        elif self.scale_image and time_now - self.time >= 10:
            self.scale_out()
            self.time = pygame.time.get_ticks()

        if time_now - self.time2 >= 100:
            self.time2 = pygame.time.get_ticks()
            self.change_background()

    
    def rotate(self):
        self.angle -= 5
        if self.angle <= -360:
            self.delay += 1500
            self.angle = 0
            self.scale_image = True
        self.letsplay_bg = pygame.transform.rotate(self.original_letsplay, self.angle)
    
    def scale_out(self):
        
        if self.scale == 0:
            self.scale_image = False
            self.scale = 5
        elif self.is_zooming and self.scale <= self.MAX_SCALE:
            self.scale += 5
            self.is_zooming = True
        else:
            self.scale -= 5
            self.is_zooming = False

        coord = self.lets_play_image_coord()
        self.letsplay_bg = pygame.transform.scale(self.original_letsplay, (self.original_letsplay.get_width() + self.scale, self.original_letsplay.get_height() + self.scale))
    
    def change_background(self):
        if self.init_bg:
            self.static_bg = pygame.image.load(self.STATIC_BG2)
            self.init_bg = False
        else:
            self.static_bg = pygame.image.load(self.STATIC_BG)
            self.init_bg = True

        self.static_bg = pygame.transform.scale(self.static_bg, (self.width, self.height))

    def lets_play_image_coord(self):
        return (self.width/2 - self.letsplay_bg.get_width()/2, self.height/2 - self.letsplay_bg.get_height()/2)