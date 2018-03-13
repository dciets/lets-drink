import pygame

class player(pygame.sprite.Sprite):

    x = 0
    y = 0
    vely = 0
    velx = 0
    name = ""
    width = 0
    height = 0
    jump_speed = 0
    gravity = 9800
    is_alive = True
    touch_the_edge = False

    def __init__(self, width, height, start_pos, velx, image, name):

        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.velx = velx
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.set_colorkey((255,255,255))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name

    def get_position(self):
        return self.x, self.y

    #calculating the hitbox with some pixel perfect adjustement
    def get_polygon(self):
        if self.velx > 0:
            return [(self.x + 10, self.y), (self.x + self.width, self.y + (self.height/2) - 4), (self.x + 10, self.y + self.height - 3)]
        else:
            return [(self.x + self.width - 10, self.y), (self.x, self.y + (self.height/2) - 4), (self.x + self.width - 10, self.y + self.height - 3)]

    def jump(self):
        self.vely = self.jump_speed

    def update_y_velocity(self, t):
        self.vely = self.vely + self.gravity * t

    def update_y_position(self, t):
        self.y = self.y + self.vely * t
        self.rect.y = self.y

    def update_x_position(self, max_width):
        self.x += self.velx
        self.rect.x = self.x

        if self.x < 0 or self.x > max_width - self.width:
            self.velx *= -1
            self.image = pygame.transform.flip(self.image, True, False)
            self.mask = pygame.mask.from_surface(self.image)
            self.touch_the_edge = True
    
    def is_on_edge(self):
        on_edge = self.touch_the_edge
        if on_edge:
            self.touch_the_edge = False
        return on_edge