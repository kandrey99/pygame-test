# import pymunk               # Import pymunk..
#
# space = pymunk.Space()      # Create a Space which contain the simulation
# space.gravity = 0,-1000     # Set its gravity
#
# body = pymunk.Body(1,1666)  # Create a Body with mass and moment
# body.position = 50,100      # Set the position of the body
#
# poly = pymunk.Poly.create_box(body) # Create a box shape and attach to body
# space.add(body, poly)       # Add both body and shape to the simulation
#
# print_options = pymunk.SpaceDebugDrawOptions() # For easy printing
#
# while True:                 # Infinite loop simulation
#     space.step(0.02)        # Step the simulation one step forward
#     space.debug_draw(print_options) # Print the state of the simulation


""" Pygame boilerplate. <ninmonkey>2011/04
        pygame main Game() loop, and numpy for vector math.

note:
        this might not be the most effecient way to use numpy as vectors, but it an intro.

        And this does not force fixed-timesteps. If you want a stable simulation, you need to use a fixed timestep.
        see: http://gafferongames.com/game-physics/fix-your-timestep/

Keys:
    ESC : exit
    Space : game_init()
"""

import sys
import pygame
from pygame.locals import *
from pygame import Color, Rect
import numpy as np


def get_screen_size():
    """return screen (width, height) tuple"""
    screen = pygame.display.get_surface()
    return screen.get_size()


class Actor:
    """basic actor, moves randomly.

    members:
        loc = position vector
        velocity = velocity vector
        width, height
    """

    def __init__(self, loc=None, velocity=None):
        """optional initial loc and velocity vectors"""
        self.width = 50
        self.height = 50

        # if loc or velocity are not set: use random
        if loc is None:
            self.rand_loc()
        else:
            self.loc = loc

        if velocity is None:
            self.rand_velocity()
        else:
            self.velocity = velocity

    def update(self):
        """update movement"""
        self.loc += self.velocity

    def rand_velocity(self):
        """set a random vector , based on random direction. Using unit circle:
                x = cos(deg) * speed
        """
        rad = np.radians(np.random.randint(0, 360))
        speed = np.random.randint(1, 15)
        x = np.cos(rad)
        y = np.sin(rad)
        velocity = np.array([x, y])
        velocity *= speed
        self.velocity = velocity

    def rand_loc(self):
        """random location onscreen"""
        width, height = get_screen_size()
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        self.loc = np.array([x, y], dtype=np.float64)

    def is_onscreen(self):
        """test is screen.colliderect(actor) true?"""
        x, y = self.loc
        w, h = get_screen_size()

        screen = Rect(0, 0, w, h)
        actor = Rect(x, y, self.width, self.height)

        if screen.colliderect(actor):
            return True
        else:
            return False


class GameMain():
    """game Main entry point. handles intialization of game and graphics."""
    done = False
    debug = False
    color_gray = Color('lightgray')

    def __init__(self, width=800, height=600, color_bg=None):
        """Initialize PyGame"""
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("boilerplate : pygame")

        self.clock = pygame.time.Clock()
        self.limit_fps = True
        self.limit_fps_max = 60

        if color_bg is None: color_bg = Color(50, 50, 50)
        self.color_bg = color_bg

        self.game_init()

    def game_init(self):
        """new game/round"""
        self.actors = [Actor() for x in range(10)]

    def loop(self):
        """Game() main loop"""
        while not self.done:
            self.handle_events()
            self.update()
            self.draw()

            if self.limit_fps:
                self.clock.tick(self.limit_fps_max)
            else:
                self.clock.tick()

    def update(self):
        """update actors, handle physics"""
        for a in self.actors:
            a.update()

            if not a.is_onscreen():
                a.rand_loc()

    def handle_events(self):
        """handle regular events. """
        events = pygame.event.get()
        # kmods = pygame.key.get_mods() # key modifiers

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    self.done = True
                elif (event.key == K_SPACE):
                    self.game_init()

    def draw(self):
        """render screen"""
        # clear screen
        self.screen.fill(self.color_bg)

        # Actor: draw
        for a in self.actors:
            x, y = a.loc
            w, h = a.width, a.height
            r = Rect(x, y, w, h)
            self.screen.fill(self.color_gray, r)

        # will call update on whole screen Or flip buffer.
        pygame.display.flip()


if __name__ == '__main__':
    g = GameMain()
    g.loop()
