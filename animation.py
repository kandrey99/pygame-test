import pygame


class Animation:
    def __init__(self, images, framerate=10, repeat=0):
        self._images = images
        self._framerate = framerate
        self._frame_duration = 1000 // self._framerate
        self._repeat = repeat
        self._last_update = pygame.time.get_ticks()
        self._current_frame = 0

    def get_image(self):
        now = pygame.time.get_ticks()
        elapsed = now - self._last_update
        if elapsed >= self._frame_duration:
            self._current_frame += (elapsed // self._frame_duration)
            if self._current_frame >= len(self._images):
                if not self._repeat:
                    return None
                if self._repeat > 0:
                    self._repeat -= 1
                self._current_frame = self._current_frame % len(self._images)
            self._last_update = now
        return self._images[self._current_frame]
