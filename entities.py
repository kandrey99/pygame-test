import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame.font import Font
from constants import *
import resources as rc
from path import Path
from animation import Animation
import math


class Player(Sprite):
    def __init__(self, path, velocity):
        super().__init__()
        self._path = Path(path, velocity)
        self.images = (pygame.transform.rotate(rc.get_image('playerShip1_blue.png'), -90),
                       rc.get_image('playerShip1_blue.png'))
        self._animation = Animation(self.images, repeat=-1)
        # self._image = pygame.transform.rotate(rc.get_image('playerShip1_blue.png'), -90)
        # self.image = self._image
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=path[0])

    def update(self, *args):
        self.rect.center = self._path.get_position()
        self.image = self._animation.get_image()
        self.image = pygame.transform.rotate(self.image, math.degrees(-self._path.slope))
        self.rect = self.image.get_rect(center=self.rect.center)


class TextPanel(Sprite):
    def __init__(self):
        super().__init__()
        self._image = Surface((130, 50))
        self._image.fill(RED)
        font = Font(pygame.font.match_font('arial'), 18)
        font_sc = font.render('Привет', 1, GREEN)
        self._image.blit(font_sc, font_sc.get_rect(center=self._image.get_rect().center))
