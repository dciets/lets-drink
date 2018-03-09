import pygame
class background:
    BACKGROUND_SPRITE = "sprites/background.png"
    def __init__(self, width, height):
        self.image = pygame.image.load(self.BACKGROUND_SPRITE)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0,0)