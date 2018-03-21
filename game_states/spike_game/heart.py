import pygame.gfxdraw

class Heart:

    #The color parameter is a tuple. Ex: (200, 0, 0) for red-ish
    def __init__(self, x, y, color):
        self.color = color
        self.points = [
            (x, y), 
            (x + 2, y - 2), 
            (x + 5, y - 2), 
            (x + 7, y), 
            (x + 9, y - 2), 
            (x + 12, y - 2), 
            (x + 14, y), 
            (x + 14, y + 3), 
            (x + 7, y + 10), 
            (x, y + 3)
        ]    

    def draw(self, screen, full):
        if full:
            pygame.gfxdraw.filled_polygon(screen, self.points, self.color)
        else:
            pygame.gfxdraw.polygon(screen, self.points, self.color) 