import pygame

class spike:

    SPIKE_SPRITE = "sprites/spike1.png"

    def __init__(self, width, height, polygon, position):
        self.width = width
        self.height = height
        self.polygon = polygon
        self.position = position
        self.image = pygame.image.load(self.SPIKE_SPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def get_x(self):
        return self.polygon[0][0]

    def get_y(self):
        return self.polygon[0][1]

    def get_spike_image(self):

        return self.image
       