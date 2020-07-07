import pygame
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

    @staticmethod
    def _get_distance(point1, point2):
        return math.hypot(point2[0] - point1[0], point2[1] - point1[1])

    @property
    def slope(self):
        return math.atan2(self._next_point[1] - self._position[1],
                          self._next_point[0] - self._position[0])

    def get_position(self):
        now = pygame.time.get_ticks()
        elapsed = now - self._last_update
        self._last_update = now
        for _ in range(elapsed // self._step):
            dv = self._step * self._velocity / 1000
            dx, dy = dv * math.cos(self.slope), dv * math.sin(self.slope)
            distance = self._get_distance(self._prev_point, self._next_point)
            distance2 = self._get_distance(self._prev_point, (self._position[0] + dx, self._position[1] + dy))
            if distance2 >= distance:
                self._index = self._index + 1
                self._prev_point = self._path[self._index]
                self._next_point = self._path[self._index + 1]
                self._position = self._prev_point
            else:
                self._position = self._position[0] + dx, self._position[1] + dy
        return self._position
