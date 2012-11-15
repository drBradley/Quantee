# -*- coding: utf-8 -*-


import pygame

from engine import Engine

__all__ = ['SDL', 'EventManager']


class SDL(Engine):
    """SDL(title, (width, height), event_manager[, fullscreen[, max_fps[,
    use_busy_loop]]]) -> the Engine

    Engine based on the PyGame binding to the SDL library.

      * `event_manager` is to be an instance of `sdl.EventManager`

      * `fullscreen` defaults to False and `max_fps` defaults to 32

      * `use_busy_loop` sets whether the clock system should actively loop
        while waiting, or use the OS level sleep mechanism. The first uses more
        CPU cycles and is more precise. The second is a smaller strain on the
        machine but less precise.

        Defaults to False.
    """

    def __init__(self, title, screen_size, event_manager, fullscreen=False,
            max_fps=32, use_busy_loop=False):

        # Prerequisite initialisation
        super(SDL, self).__init__()

        pygame.init()

        # Prepare for rendering
        pygame.display.set_mode(
                screen_size,
                pygame.FULLSCREEN if fullscreen else 0)

        self.__screen = pygame.display.get_surface()

        pygame.display.set_caption(title)

        self.__sprite_cache = {}

        # Prepare the event system
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(event_manager.allowed)

        self.__event_manager = event_manager

        # Prepare SDL-based clock system
        self.__clock = pygame.time.Clock()
        self.__max_fps = max_fps
        self.__use_busy_loop = use_busy_loop

    # Input and time
    def input(self):
        """E.input() -> an Event or None"""

        raw_event = pygame.event.poll()

        event = self.__event_manager.transform(raw_event)

        return event

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

        if self.__use_busy_loop:

            return self.__clock.tick_busy_loop(self.__max_fps)

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


class EventManager(object):
    """Abstract base class for EventManagers."""

    @property
    def allowed(self):
        """EM.allowed

        Property, returning a list of allowed event types (configured per
        class). Subclasses may decide to use a more sophisticated mechanism of
        determining gets into it's value.
        """

        raise NotImplementedError()

    def transform(self, raw_event):
        """EM.transform(raw_event) -> event

        Take a PyGame event and return a one tailored to the needs of a
        particular game.
        """

        raise NotImplementedError()
