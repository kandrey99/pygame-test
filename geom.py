import pygame as pg
import math

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255


class Circle:
    def __init__(self):
        self._radius = 100
        self._rot = 0
        self._rot_speed = math.pi / 2
        self._wave = list()
        self.image = pg.Surface((800, 800))
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.image.fill(BLACK)
        self._rot -= (self._rot_speed * dt / 1000) % 360
        x = round(self._radius * math.cos(self._rot))
        y = round(self._radius * math.sin(self._rot))
        self._wave.append((x, y))
        for i, p in enumerate(self._wave):
            pg.draw.circle(self.image, GREEN, (300 + i, 150 + p[1]), 1)
            pg.draw.circle(self.image, RED, (150 + p[0], 300 + i), 1)
        pg.draw.circle(self.image, WHITE, (150, 150), self._radius, 1)
        pg.draw.circle(self.image, WHITE, (150 + x, 150 + y), 7)
        pg.draw.line(self.image, WHITE, (150, 150), (150 + x, 150 + y))  # radius
        pg.draw.line(self.image, BLUE, (150 + x, 150 + y), (300 + len(self._wave), 150 + self._wave[len(self._wave) - 1][1]))
        pg.draw.line(self.image, BLUE, (150 + x, 150 + y), (150 + self._wave[len(self._wave) - 1][0], 300 + len(self._wave)))
        if len(self._wave) > 400:
            self._wave.pop()


class App:
    def __init__(self):
        self._size = self._weight, self._height = 800, 800
        self._screen = pg.display.set_mode(self._size, pg.HWSURFACE | pg.DOUBLEBUF)
        self._keys = pg.key.get_pressed()
        self._clock = pg.time.Clock()
        self._running = True
        self._circle = Circle()

    def _event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            if event.type in (pg.KEYUP, pg.KEYDOWN):
                self._keys = pg.key.get_pressed()

    def _update(self, dt):
        self._circle.update(dt)

    def _render(self):
        self._screen.fill(WHITE)
        self._screen.blit(self._circle.image, self._circle.rect)
        pg.display.flip()

    def run(self):
        while self._running:
            self._event_loop()
            dt = self._clock.tick(30)
            self._update(dt)
            self._render()


if __name__ == '__main__':
    app = App()
    app.run()
