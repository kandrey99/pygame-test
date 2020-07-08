import pygame
import math


class AbstractPath:
    """
    velocity: px/s
    start: start point
    stop: stop point
    """

    def __init__(self, velocity, start, stop):
        self._velocity = velocity
        self._start = start
        self._stop = stop
        self._current = start
        self._last_update = pygame.time.get_ticks()

    def _set_line(self):
        self._start, self._stop = self._stop, self._start

    @staticmethod
    def _get_distance(start, stop):
        return math.hypot(stop[0] - start[0], stop[1] - start[1])

    @property
    def slope(self):
        return math.atan2(self._stop[1] - self._current[1],
                          self._stop[0] - self._current[0])

    def get_position(self):
        now = pygame.time.get_ticks()
        elapsed = now - self._last_update
        self._last_update = now
        while True:
            dist = self._get_distance(self._current, self._stop)
            time = dist * 1000 / self._velocity
            if elapsed > time:
                self._set_line()
                self._current = self._start
                elapsed -= time
            else:
                dv = elapsed * self._velocity / 1000
                dx, dy = dv * math.cos(self.slope), dv * math.sin(self.slope)
                self._current = self._current[0] + dx, self._current[1] + dy
                break
        return self._current


class Path(AbstractPath):
    def __init__(self, velocity, path):
        super().__init__(velocity, path[0], path[1])
        self._path = path
        self._index = 0

    def _set_line(self):
        self._index += 1
        self._start = self._path[self._index]
        if self._index + 1 < len(self._path):
            self._stop = self._path[self._index + 1]
        else:
            self._index = -1
            self._stop = self._path[0]
