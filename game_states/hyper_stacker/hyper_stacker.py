from controller import Controller
import pygame
import pygame.gfxdraw
import yaml
from random import randint
from copy import deepcopy

class Heart:

    def __init__(self, x, y):
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
            pygame.gfxdraw.filled_polygon(screen, self.points, (200, 0, 0))
        else:
            pygame.gfxdraw.polygon(screen, self.points, (200, 0, 0))            

class Rectangle:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = 60
        self.width = width
        self.height = height
        self.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        self.going_right = True
        self.moving = True

    def draw(self, screen, i):
        y = self.y if i < 0 else 549 - self.height*(i + 1)
        pygame.draw.rect(screen, self.color, [self.x, y, self.width, self.height])

    def update(self):
        if self.moving:
            if self.going_right:
                self.x += 5
            else:
                self.x -= 5

class HyperStacker:

    ITEM_FOREGROUND_COLOR = (100, 150, 255)
    ITEM_FOREGROUND_COLOR_SELECTED = (255, 255, 255)

    def __init__(self, game, teams):
        self.team1, self.team2 = teams
        self.game = game
        self.direction1 = True
        self.direction2 = True
        self.shapes1 = []
        self.shapes2 = []
        self.current_shape1 = Rectangle(0, 60, 100, 50)
        self.current_shape2 = Rectangle(387, 60, 100, 50)
        self.game_over1 = False
        self.game_over2 = False
        self.max_lives = 3

        self.lives1 = self.max_lives
        self.lives2 = self.max_lives

        self.score1 = 0
        self.score2 = 0

        self.shapes1.append(Rectangle((363 - 200)/2, 549 - 50, 200, 50))
        self.shapes2.append(Rectangle((363 - 200)/2 + 387, 549 - 50, 200, 50))

    def get_next_width(self, shapes):
        first_bound = [shape.x for shape in shapes]
        second_bound = [shape.x + shape.width for shape in shapes]
        return min(second_bound) - max(first_bound)
    
    def get_next_x(self, shapes):
        return max([shape.x for shape in shapes])

    def run(self):
        self.game.screen.fill((0,0,0))

        pygame.draw.rect(self.game.screen, (255, 255, 255), (0, 40, 363, 510), 1)
        pygame.draw.rect(self.game.screen, (255, 255, 255), (387, 40, 363, 510), 1)

        textsurface = self.game.font.render(self.team1, True, HyperStacker.ITEM_FOREGROUND_COLOR)
        x = (363 - textsurface.get_width())/2
        y = 0
        self.game.screen.blit(textsurface, (x, y))

        textsurface = self.game.font.render(self.team2, True, HyperStacker.ITEM_FOREGROUND_COLOR)
        x = (363 - textsurface.get_width())/2 + 387
        y = 0
        self.game.screen.blit(textsurface, (x, y))

        for evt in pygame.event.get([Controller.BUTTON_PRESSED, Controller.BUTTON_RELEASED]):

            if evt.type == Controller.BUTTON_PRESSED and evt.index == Controller.BUTTON1:
                if not self.game_over1:
                    self.current_shape1.moving = False
                    next_x = self.get_next_x(self.shapes1)
                    next_width = self.get_next_width(self.shapes1 + [self.current_shape1])
                    if next_width > 0:
                        if self.current_shape1.x < next_x:
                            self.current_shape1.x = next_x
                        self.current_shape1.width = next_width
                        self.shapes1.append(deepcopy(self.current_shape1))
                        if len(self.shapes1) > 3:
                            self.shapes1.pop(0)
                        self.current_shape1 = Rectangle(0, 60, next_width, 50)
                        self.score1 += 10
                    else:
                        self.lives1 -= 1
                        self.game_over1 = True

            if evt.type == Controller.BUTTON_RELEASED and evt.index == Controller.BUTTON1:
                pass

            if evt.type == Controller.BUTTON_PRESSED and evt.index == Controller.DRINK1:
                if self.lives1 > 0 and self.game_over1:
                    self.shapes1 = []
                    self.current_shape1 = Rectangle(0, 60, 100, 50)
                    self.game_over1 = False
                    self.shapes1.append(Rectangle((363 - 200)/2, 549 - 50, 200, 50))

            if evt.type == Controller.BUTTON_PRESSED and evt.index == Controller.BUTTON2:
                if not self.game_over2:
                    self.current_shape2.moving = False
                    next_x = self.get_next_x(self.shapes2)
                    next_width = self.get_next_width(self.shapes2 + [self.current_shape2])
                    if next_width > 0:
                        if self.current_shape2.x < next_x:
                            self.current_shape2.x = next_x
                        self.current_shape2.width = next_width
                        self.shapes2.append(deepcopy(self.current_shape2))
                        if len(self.shapes2) > 3:
                            self.shapes2.pop(0)
                        self.current_shape2 = Rectangle(387, 60, next_width, 50)
                        self.score2 += 10
                    else:
                        self.lives2 -= 1
                        self.game_over2 = True

            if evt.type == Controller.BUTTON_RELEASED and evt.index == Controller.BUTTON2:
                pass

            if evt.type == Controller.BUTTON_PRESSED and evt.index == Controller.DRINK2:
                if self.lives2 > 0 and self.game_over2:
                    self.shapes2 = []
                    self.current_shape2 = Rectangle(387, 60, 100, 50)
                    self.game_over2 = False
                    self.shapes2.append(Rectangle((363 - 200)/2 + 387, 549 - 50, 200, 50))

        if self.current_shape1.x + self.current_shape1.width >= 363 or self.current_shape1.x < 0:
            self.current_shape1.going_right = not self.current_shape1.going_right

        if self.current_shape2.x + self.current_shape2.width >= 750 or self.current_shape2.x < 387:
            self.current_shape2.going_right = not self.current_shape2.going_right

        self.current_shape1.update()
        self.current_shape1.draw(self.game.screen, -1)

        self.current_shape2.update()
        self.current_shape2.draw(self.game.screen, -1)
        
        #Draws the lives
        for i in xrange(self.max_lives):
            #team 1
            Heart(i*20, 6).draw(self.game.screen, self.lives1 > i)
            #team 2
            Heart(i*20 + 387, 6).draw(self.game.screen, self.lives2 > i)

        #Draws team 1's score
        textsurface = self.game.font.render("{} pts".format(self.score1), True, (255, 255, 255))
        x = 350 - textsurface.get_width()
        y = 0
        self.game.screen.blit(textsurface, (x, y))

        #Draws team 2's score
        textsurface = self.game.font.render("{} pts".format(self.score2), True, (255, 255, 255))
        x = 387 + 350 - textsurface.get_width()
        y = 0
        self.game.screen.blit(textsurface, (x, y))

        for i, shape in enumerate(self.shapes1):
            shape.draw(self.game.screen, i)

        for i, shape in enumerate(self.shapes2):
            shape.draw(self.game.screen, i)

        if self.lives1 > 0 or self.lives2 > 0:

            if self.game_over1:
                if self.lives1 <= 0:
                    textsurface = self.game.title_font.render("Game Over", True, (200, 0, 0))
                else:
                    textsurface = self.game.font.render("You've lost a life", True, (200, 0, 0))                
                x = (363 - textsurface.get_width())/2
                y = 200
                self.game.screen.blit(textsurface, (x, y))

            if self.game_over2:
                if self.lives2 <= 0:
                    textsurface = self.game.title_font.render("Game Over", True, (200, 0, 0))
                else:
                    textsurface = self.game.font.render("You've lost a life", True, (200, 0, 0))
                x = (363 - textsurface.get_width())/2 + 387
                y = 200
                self.game.screen.blit(textsurface, (x, y))

        else:

            text = "It's a TIE" if self.score1 == self.score2 else (self.team1 if self.score1 > self.score2 else self.team2) + " wins!"
            textsurface = self.game.title_font.render(text, True, (255, 255, 255))

            x = (363 - textsurface.get_width())/2
            y = 200
            self.game.screen.blit(textsurface, (x, y))

            x = (363 - textsurface.get_width())/2 + 387
            y = 200
            self.game.screen.blit(textsurface, (x, y))

            self.game.end_game(players=[self.team1, self.team2], winners=[self.score1 > self.score2, self.score2 > self.score1])