# -*- coding: utf-8 -*-


import pygame

from engine import Engine
__all__ = ['SDL']


class SDL(Engine):
    """SDL(title, (width, height)[, fullscreen[, max_fps]])
    -> the Engine

    Engine based on the PyGame binding to the SDL library.

    `fullscreen` defaults to False and `max_fps` defaults to 32.
    """

    def __init__(self, title, screen_size, fullscreen=False, max_fps=32):

        # Prerequisite initialisation
        super(Engine, self).__init__()

        pygame.init()

        # Prepare for rendering
        pygame.display.set_mode(
                screen_size,
                pygame.FULLSCREEN if fullscreen else 0)

        self.__screen = pygame.display.get_surface()

        pygame.display.set_caption(title)

        self.__sprite_cache = {}

        # Prepare SDL-based clock system
        self.__clock = pygame.time.Clock()
        self.__max_fps = max_fps

    # Input and time
    def input(self):
        """E.input() -> an Event or None"""

        raise NotImplementedError()

    def tick(self):
        """E.tick()

        Needs to be called every loop iteration to keep the internal
        clock running.
        """

        pass

    @property
    def dt(self):
        """E.dt

        The time since the last call to tick.
        """

        return self.__clock.tick(self.__max_fps)

    # Rendering
    @property
    def screen_size(self):
        """E.screen_size -> (width, height)"""

        return self.__screen.get_size()

    def draw(self, pos, sprite_name, rect=None):
        """E.draw((x, y), sprite_name[, Box(x_sub, y_sub, w_sub, h_sub)])

        Draws the sprite named sprite_name at the (x, y) coordinates of the
        window.

        The optional Box describes which subset of the sprite to draw. When not
        specified, the whole sprite is drawn.

        The coordinates are standard Cartesian. It's the Engine's job to
        transform them to the underlying coordinate system used by the
        rendering library.
        """

        raise NotImplementedError()
