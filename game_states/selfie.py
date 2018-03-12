from controller import Controller
import pygame
import pygame.camera
import menu

class Selfie:
    def __init__(self, game):
        self.game = game
        self.size = (1280, 1024)
        self.cam = pygame.camera.Camera('/dev/video0', self.size)
        self.cam.start()
        self.snapshot = False
        self.start_time = None
        self.take_photo = False

        self.font = pygame.font.SysFont('DroidSans', 150)

        self.raw = pygame.surface.Surface(self.size, 0, self.game.border)

    def run(self):
        if self.take_photo:
            self.game.screen.fill((255, 255, 255))

            pygame.display.update()

            flash_start = pygame.time.get_ticks()

            while pygame.time.get_ticks() - flash_start < 2000:
                self.raw = self.cam.get_image(self.raw)

            pygame.image.save(self.raw, "image.jpg")

            for evt in pygame.event.get():
                pass

            self.game.state = menu.Menu(self.game)
            
            return

        if self.cam.query_image():
            self.raw = self.cam.get_image(self.raw)
            self.snapshot = pygame.transform.scale(self.raw, (800, 600))

            if not self.start_time:
                self.start_time = pygame.time.get_ticks()

        if self.snapshot:
            self.game.border.blit(self.snapshot, (0,0))

        if self.start_time:
            elapsed = 6 - int((pygame.time.get_ticks() - self.start_time) / 1000)

            textsurface = self.font.render(str(elapsed), False, (255, 255, 0))

            self.game.border.blit(textsurface, (300, 300))

            if elapsed == 0:
                self.take_photo = True

        for evt in pygame.event.get():
            pass
