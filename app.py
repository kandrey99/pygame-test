import pygame
from entities import *

pygame.init()
pygame.font.init()


class App:
    def __init__(self):
        self.size = self.weight, self.height = 640, 400
        self._running = True
        self._display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._bg = rc.get_scaled_image('purple.png', self.size)
        self._clock = pygame.time.Clock()
        self._player = Player(100, [(100, 130), (320, 150)])

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self._player._path._path.append(pos)
            # print(self._player._path._path)

    def update(self):
        self._player.update()

    def render(self):
        self._display.blit(self._bg, self._bg.get_rect())
        for pos in self._player._path._path:
            pygame.draw.circle(self._display, RED, pos, 7, 1)
        self._display.blit(self._player.image, self._player.rect)
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()

    def run(self):
        while self._running:
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
            self.update()
            self.render()
        self.cleanup()
