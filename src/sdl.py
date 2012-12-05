# -*- coding: utf-8 -*-


import pygame

from boxes import Box
from engine import Engine

__all__ = ['SDL', 'EventManager']


SCALE = 1


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

    def __init__(self, title, screen_size, asset_manager, event_manager, fullscreen=False,
                 max_fps=32, use_busy_loop=False):

        # Prerequisite initialisation
        super(SDL, self).__init__()

        pygame.init()

        # Prepare the asset manager
        self.__asset_manager = asset_manager

        # Prepare for rendering
        pygame.display.set_mode(
            screen_size,
            pygame.FULLSCREEN if fullscreen else 0)

        self.__screen = pygame.display.get_surface()

        pygame.display.set_caption(title)

        self.__blitted_boxes = []

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
        """SDL.input() -> an Event or None"""

        if self.__use_busy_loop:

            dt = self.__clock.tick_busy_loop(self.__max_fps)

        else:

            dt = self.__clock.tick(self.__max_fps)

        raw_event = pygame.event.poll()
        event = self.__event_manager.transform(raw_event)

        return event, dt

    def update(self):
        """SDL.update()

        Call every iteration to ensure that drawing works properly -- in PyGame
        everything is first drawn to a buffer and only later, with this,
        applied on top of the display memory.
        """

        if self.__blitted_boxes:
            pygame.display.update()
            self.__blitted_boxes = []

    # Coordinate system handling
    def __to_screen_coords(self, box, scale, viewport):
        """SDL.__to_screen_coords(box, scale, viewport) -> Box

        Given a box in the stage's coordinate system, a viewport and a scaling
        factor between units, return the equivalent box in the screen's
        coordinate system.
        """

        n_box = Box(scale * (box.x - viewport.x),
                    scale * (viewport.h + viewport.y - box.y - box. h),
                    scale * box.w,
                    scale * box.h)

        return n_box

    def __to_stage_coords(self, box, scale, viewport):
        """SDL.__to_stage_coords(box, scale, viewport) -> Box

        Given a box in the screen's coordinate system, a viewport and a scaling
        factor between units, return the equicalent box in the stage's
        coordinate system.
        """

        n_box = Box((box.x + viewport.x) / scale,
                    (viewport.h + viewport.y - box.y - box.h) / scale,
                    box.w / scale,
                    box.h / scale)

        return n_box

    # Rendering
    @property
    def screen_size(self):
        """SDL.screen_size -> (width, height)"""

        return self.__screen.get_size()

    def draw(self, pos, sprite_name, viewport):
        """SDL.draw((x, y), sprite_name, viewport)

        Draws the sprite named sprite_name at the (x, y) coordinates of the
        window.

        The optional Box describes which subset of the sprite to draw. When not
        specified, the whole sprite is drawn.

        The coordinates are standard Cartesian. It's the Engine's job to
        transform them to the underlying coordinate system used by the
        rendering library.
        """

        # Get the sprite
        sprite = self.__asset_manager.load_sprite(sprite_name)

        # Recalculate the coordinates
        x, y = pos
        coords = self.__to_screen_coords(self, Box(x, y, 0, 0), SCALE, viewport)

        # Blit to self.__screen
        self.__screen.blit(sprite, (coords.x, coords.y))

        # Remember which box was blitted
        self.__blitted_boxes.append((coords.x,
                                     coords.y,
                                     coords.w,
                                     coords.h))


class AssetManager(object):
    """Abstract base class for AssetManagers."""

    def load_sprite(self, name, no_cache=False):
        """AM.load_sprite(name[, no_cache]) -> sprite

        Load up a sprite, possibly with caching turned off.
        """

        raise NotImplementedError()

    def clear_cache(self):
        """AM.clear_cache()

        Clear the cache, so that extraneous memory isn't used.
        """

        raise NotImplementedError()


class EventManager(object):
    """Abstract base class for EventManagers."""

    @property
    def allowed(self):
        """EM.allowed

        Property, returning a list of allowed event types (configured per
        class).
        """

        raise NotImplementedError()

    def transform(self, raw_event):
        """EM.transform(raw_event) -> event

        Take a PyGame event and return a one tailored to the needs of a
        particular game.
        """

        raise NotImplementedError()
