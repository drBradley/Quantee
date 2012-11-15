# -*- coding: utf-8 -*-


import time

__all__ = ['Engine']


class Engine(object):
    """Abstract base class for engines."""

    def __init__(self):
        self.__prev = time.time()

    # Input and time
    def input(self):
        """E.input() -> an Event or None"""

        raise NotImplementedError()

    def tick(self):
        """E.tick()

        Needs to be called every loop iteration to keep the internal
        clock running.
        """

        self.__prev = time.time()

    @property
    def dt(self):
        """E.dt

        The time since the last call to tick.
        """

        return time.time() - self.__prev

    # Rendering
    @property
    def screen_size(self):
        """E.screen_size -> (width, height)"""

        raise NotImplementedError()

    def draw(self, pos, sprite_name, rect=None):
        """E.draw((x, y), sprite_name[, (x_sub, y_sub, w_sub, h_sub)])

        Draws the sprite named sprite_name at the (x, y) coordinates of the
        window.

        The optional four element tuple describes which subset of the sprite to
        draw. When not specified, the whole sprite is drawn.

        The coordinates are standard Cartesian. It's the Engine's job to
        transform them to the underlying coordinate system used by the
        rendering library.
        """

        raise NotImplementedError()
