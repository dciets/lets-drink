from pygame import transform
import math

class player:

    x = 0
    y = 0
    vely = 0
    velx = 0
    name = ""
    width = 0
    height = 0
    jump_speed = 0
    gravity = 9000
    is_alive = True
    touch_the_edge = False

    def __init__(self, width, height, start_pos, velx, image, name):

        self.width = width
        self.height = height
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.velx = velx
        self.image = image
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

    def update_x_position(self, max_width):
        self.x += self.velx
        if self.x < 0 or self.x > max_width - self.width:
            self.velx *= -1
            self.x = 5 if self.x < 0 else max_width - self.width - 5
            self.image = transform.flip(self.image, True, False)
            self.touch_the_edge = True
            self.update_speed()
    
    def update_speed(self):
        abs_velx = abs(self.velx)
        self.velx += math.log(abs_velx, 2) ** -1 if self.velx > 0 else -math.log(abs_velx, 2) ** -1
    
    def is_on_edge(self):
        on_edge = self.touch_the_edge
        if on_edge:
            self.touch_the_edge = False
        return on_edge
       