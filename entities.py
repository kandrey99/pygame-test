import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame.font import Font
from constants import *
import math


class Path:
    """
    path: list of points
    velocity: px/s
    """
    def __init__(self, path, velocity):
        self._path = path
        self._velocity = velocity
        self._index = 0
        self._prev_point = self._path[self._index]
        self._next_point = self._path[self._index + 1]
        self._position = self._prev_point
        self._last_update = pygame.time.get_ticks()
        self._step = 10  # ms

    @property
    def slope(self):
        return math.atan2(self._next_point[1] - self._position[1],
                          self._next_point[0] - self._position[0])

    @property
    def distance(self):
        return math.hypot(self._next_point[0] - self._prev_point[0],
                          self._next_point[1] - self._prev_point[1])

    @property
    def distance2(self):
        return math.hypot(self._position[0] - self._prev_point[0],
                          self._position[1] - self._prev_point[1])

    def get_position(self):
        now = pygame.time.get_ticks()
        elapsed = now - self._last_update
        for _ in range(elapsed // self._step):
            if self.distance2 >= self.distance:
                self._index = self._index + 1
                self._prev_point = self._path[self._index]
                self._next_point = self._path[self._index + 1]
            dv = self._step * self._velocity / 1000
            dx, dy = dv * math.cos(self.slope), dv * math.sin(self.slope)
            self._position = self._position[0] + dx, self._position[1] + dy
        self._last_update = now
        return self._position


class Player(Sprite):
    def __init__(self, path, velocity):
        super().__init__()
        self._path = Path(path, velocity)
        self._image = Surface((130, 50)).convert_alpha()
        self._image.fill(RED)
        font = Font(pygame.font.match_font('arial'), 18)
        font_sc = font.render('Привет', 1, GREEN)
        self._image.blit(font_sc, font_sc.get_rect(center=self._image.get_rect().center))
        self.image = self._image
        self.rect = self.image.get_rect(center=path[0])

    def update(self, *args):
        self.rect.center = self._path.get_position()
        if abs(self._path.slope) > math.pi / 2:
            self.image = pygame.transform.flip(self._image, True, False)
        else:
            self.image = self._image
        # self.image = pygame.transform.rotate(self._image, (self._path.slope % (math.pi / 2)) * 57)
        self.rect = self.image.get_rect(center=self.rect.center)
