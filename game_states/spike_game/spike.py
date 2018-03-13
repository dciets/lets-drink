import pygame

class spike(pygame.sprite.Sprite):

    SPIKE_SPRITE = "sprites/spike1.png"
    SPIKE_POSITION = ["TOP", "BOTTOM", "LEFT", "RIGHT"]
    y_offset = 0
    x_offset = 0

    def __init__(self, width, height, polygon, position):

        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height
        self.polygon = polygon
        self.position = position
        self.image = pygame.image.load(self.SPIKE_SPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if position == self.SPIKE_POSITION[1]:
            self.image = pygame.transform.flip(self.image, False, True)
            self.y_offset = -self.height
        elif position == self.SPIKE_POSITION[2]:
            self.image = pygame.transform.rotate(self.image, 90)
        elif position == self.SPIKE_POSITION[3]:
            self.image = pygame.transform.rotate(self.image, 270)
            self.x_offset = -self.height

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((255,255,255))
        self.rect.x = self.get_x()
        self.rect.y = self.get_y()

    def get_x(self):
        return self.polygon[0][0] + self.x_offset

    def get_y(self):
        return self.polygon[0][1] + self.y_offset 

    def get_spike_image(self):
        return self.image
       