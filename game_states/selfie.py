from controller import Controller
import pygame
import pygame.camera
import menu
import time


def darken(color, factor):
    return tuple([c * (1 - factor) for c in color])

class Selfie:
    SHADOW = 8

    LOGO = "sprites/logo.png"

    def __init__(self, game, players=[], winners=[]):
        self.game = game
        self.size = (1280, 1024)
        self.cam = pygame.camera.Camera('/dev/video0', self.size)
        self.cam.start()
        self.snapshot = False
        self.start_time = None
        self.take_photo = False

        self.timer_font = pygame.font.SysFont('DroidSans', 200, True)
        self.team_font = pygame.font.SysFont('DroidSans', 50, True)

        self.raw = pygame.surface.Surface(self.size, 0, self.game.border)

        self.players = players or ['Sherbrooke', 'Polytechnique']
        self.winners = winners or [True, False]
        self.logo = pygame.image.load(self.LOGO)
        self.logo = pygame.transform.scale(self.logo, (self.game.screen.get_width() / 4, self.game.screen.get_height() / 4))

    def render_overlay(self, surface):
        colors = [(22, 105, 249), (64, 249, 22)]

        for i in range(2):
            textsurface = self.team_font.render(self.players[i], False, darken(colors[i], 0.8))

            (x, y) = ((0.25 + i * 0.5) * self.game.SCREEN_WIDTH - textsurface.get_width() / 2, self.game.SCREEN_HEIGHT * 0.10)

            for d in range(1, self.SHADOW):
                surface.blit(textsurface, (x + d, y + d))

            textsurface = self.team_font.render(self.players[i], False, colors[i])
            surface.blit(textsurface, (x, y))

            if self.winners[i]:
                color = (64, 249, 22)
                textsurface = self.team_font.render("WIN", False, darken(color, 0.8))
                (x, y) = ((0.25 + i * 0.5) * self.game.SCREEN_WIDTH - textsurface.get_width() / 2, self.game.SCREEN_HEIGHT * 0.2)

                for d in range(1, self.SHADOW):
                    surface.blit(textsurface, (x + d, y + d))

                textsurface = self.team_font.render("WIN", False, color)
                surface.blit(textsurface, (x, y))
        
        self.draw_logo(surface)

    def draw_logo(self, surface):
        surface.blit(self.logo, self.lets_play_image_coord())
    
    def lets_play_image_coord(self):
        return (self.game.screen.get_width()/2 - self.logo.get_width()/2, self.game.screen.get_height ()- self.logo.get_height())

    def run(self):
        if self.take_photo:
            self.game.border.fill((255, 255, 255))

            pygame.display.update()

            flash_start = pygame.time.get_ticks()

            while pygame.time.get_ticks() - flash_start < 2000:
                self.raw = self.cam.get_image(self.raw)

            self.snapshot = pygame.transform.scale(self.raw, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
            self.snapshot = pygame.transform.flip(self.snapshot, True, False)

            self.render_overlay(self.snapshot)

            file_name = time.strftime('pictures/%Y-%m-%d-%H-%M.jpg')

            pygame.image.save(self.snapshot, file_name)

            for evt in pygame.event.get():
                pass

            self.game.border.fill((0, 0, 0))
            self.game.state = menu.Menu(self.game)
            self.cam.stop()

            return

        if self.cam.query_image():
            self.raw = self.cam.get_image(self.raw)
            self.snapshot = pygame.transform.scale(self.raw, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
            self.snapshot = pygame.transform.flip(self.snapshot, True, False)

            if not self.start_time:
                self.start_time = pygame.time.get_ticks()

        if self.snapshot:
            self.render_overlay(self.snapshot)
            self.game.border.blit(self.snapshot, (0,0))

        if self.start_time:
            elapsed = 5 - int((pygame.time.get_ticks() - self.start_time) / 1000)
            textsurface = self.timer_font.render(str(elapsed), False, (255, 255, 255))

            self.game.border.blit(textsurface, (self.game.SCREEN_WIDTH / 2 - textsurface.get_width() / 2, self.game.SCREEN_HEIGHT / 2 - textsurface.get_height() / 2))

            if elapsed == 0:
                self.take_photo = True

        for evt in pygame.event.get():
            pass
