import pygame as pg
from collections import namedtuple
import math

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
GRAY = 64, 64, 64

Point = namedtuple('Point', 'x y')
Vector = namedtuple('Vector', 'cos sin')


class Circle:
    def __init__(self):
        self._radius = 100
        self._center = Point(150, 150)
        self._rot = 0
        self._rot_speed = math.pi / 120
        self._dot = None
        self._vector = None
        self._wave = list()
        self._margin = Point(self._center.x + self._radius + 50, self._center.y + self._radius + 50)
        self.image = pg.Surface((800, 800))
        self.rect = self.image.get_rect()

    def _draw_axis(self):
        pg.draw.line(self.image, GRAY, (self._center.x - self._radius, self._center.y),
                     (self._margin.x + 450, self._center.y))
        pg.draw.line(self.image, GRAY, (self._center.x, self._center.y - self._radius),
                     (self._center.x, self._margin.y + 450))

    def _draw_text(self):
        font = pg.font.Font(pg.font.match_font('arial'), 18)
        text = (f'rot: {math.degrees(2 * math.pi - self._rot):8.2f}'
                f'  cos: {self._vector.cos / self._radius:7}  sin: {-self._vector.sin / self._radius:7}')
        sc = font.render(text, True, WHITE)
        self.image.blit(sc, sc.get_rect(topleft=(5, 5)))

    def _draw_circle(self):
        pg.draw.circle(self.image, WHITE, self._center, self._radius, 1)  # circle
        pg.draw.circle(self.image, WHITE, self._dot, 7)  # dot
        pg.draw.line(self.image, WHITE, self._center, self._dot)  # radius

    def _draw_func(self):
        for i, p in enumerate(self._wave):
            pg.draw.circle(self.image, GREEN, (self._margin.x + 400 - i, p.y), 1)  # sin
            pg.draw.circle(self.image, RED, (p.x, self._margin.y + 400 - i), 1)  # cos
        pen_sin = self._margin.x + 400, self._wave[0].y
        pen_cos = self._wave[0].x, self._margin.y + 400
        pg.draw.line(self.image, BLUE, self._dot, pen_sin)
        pg.draw.line(self.image, BLUE, self._dot, pen_cos)

    def update(self):
        self.image.fill(BLACK)
        self._draw_axis()
        self._rot = (self._rot - self._rot_speed) % (2 * math.pi)
        self._vector = Vector(round(self._radius * math.cos(self._rot)), round(self._radius * math.sin(self._rot)))
        self._dot = Point(self._center.y + self._vector.cos, self._center.x + self._vector.sin)
        self._draw_circle()
        self._wave.insert(0, self._dot)
        self._draw_func()
        if len(self._wave) > 400:
            self._wave.pop()
        self._draw_text()


class App:
    def __init__(self):
        pg.init()
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
        self._circle.update()

    def _render(self):
        self._screen.fill(WHITE)
        self._screen.blit(self._circle.image, self._circle.rect)
        pg.display.flip()

    def run(self):
        while self._running:
            self._event_loop()
            dt = self._clock.tick(5)
            self._update(dt)
            self._render()


if __name__ == '__main__':
    app = App()
    app.run()
