import pygame

class spike:

    SPIKE_SPRITE = "sprites/spike1.png"


    def __init__(self, width, height, polygone, position):
        self.width = width
        self.height = height
        self.polygone = polygone
        self.position = position
        self.image = pygame.image.load(self.SPIKE_SPRITE).convert_alpha()

    def get_x(self):
        return self.polygone[0][0]

    def get_y(self):
        return self.polygone[0][1]

    def get_spike_image(self, color):

        image = self.image.copy()
        image = pygame.transform.scale(image, (self.width, self.height))
        image.fill(color, None, pygame.BLEND_RGBA_MAX)

        return image
       