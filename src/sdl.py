# -*- coding: utf-8 -*-

# Copyright 2012-2013 Karol Marcjan and Bartosz Boguniewicz
#
# This file is part of Quantee.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.


import pygame

from frames.boxes import Box
from frames.engine import Engine, Options

__all__ = ['SDL']


SCALE = 1


class Internal(object):
    """Internal(fullscreen) -> a new Internal object

    Used to communicate between the SDL Engine class and it's Options class
    without giving either public methods to do so.
    """

    def __init__(self, fullscreen):

        self.__fullscreen = fullscreen

    def fullscreen(self):
        """I.fullscreen() -> bool

        Tells whether the engine is in fullscreen mode or not.
        """

        return self.__fullscreen

    def set_fullscreen(self, yes):
        """I.set_fullscreen(yes)

        Sets the value of the fullscreen setting, to be shared between Options
        and SDL.
        """

        self.__fullscreen = yes


class Options(Options):
    """Options(engine) -> a new Options object for the SDL engine"""

    def __init__(self, engine, internals):

        self.__engine = engine
        self.__internals = internals

        self.__fullscreen = None
        self.__resolution = None

        self.__screen_changed = False

    def screen_changed(self):

        did_it = self.__screen_changed

        self.__screen_changed = False

        return did_it

    def fullscreen(self):

        self.__internals.fullscreen()

    def set_fullscreen(self, yes):

        self.__fullscreen = yes

    def resolution(self):

        return self.__engine.screen_size()

    def set_resolution(self, width, height):

        self.__resolution = (width, height)

    def confirm(self):

        fullscreen = self.__engine.fullscreen()
        res = self.__engine.screen_size()

        call_set_mode = False

        if self.__resolution not in (None, res):

            res = self.__resolution
            call_set_mode = True

        if self.__fullscreen not in (None, fullscreen):

            fullscreen = self.__fullscreen
            call_set_mode = True

        if call_set_mode:

            pygame.display.set_mode(
                res,
                pygame.FULLSCREEN if fullscreen else 0)

            self.__internals.set_fullscreen(fullscreen)
            self.__screen_changed = True

    def cancel(self):

        self.__fullscreen = None
        self.__resolution = None


class SDL(Engine):
    """SDL(title, (width, height), color_key, asset_manager[, fullscreen[,
    max_fps[, use_busy_loop[, allowed_events]]]]) -> the Engine

    Engine based on the PyGame binding to the SDL library.

      * `color_key` is the color to be considered transparent in sprites

      * `fullscreen` defaults to False and `max_fps` defaults to 32

      * `use_busy_loop` sets whether the clock system should actively loop
        while waiting, or use the OS level sleep mechanism. The first uses more
        CPU cycles and is more precise. The second is a smaller strain on the
        machine but less precise.

        Defaults to False.

      * `allowed_events` is a list of PyGame event types that shouldn't be
        ommited. Defaults to [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]
    """

    def __init__(self, title, screen_size, color_key, asset_manager,
                 fullscreen=False, max_fps=32, use_busy_loop=False,
                 allowed_events=[pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]):

        # Prerequisite initialisation
        super(SDL, self).__init__()

        pygame.init()

        # Prepare the options object
        self.__internals = Internal(fullscreen)
        self.__opt = Options(self, self.__internals)

        # Prepare the asset manager
        self.__asset_manager = asset_manager

        # Prepare for rendering
        pygame.display.set_mode(
            screen_size,
            pygame.FULLSCREEN if fullscreen else 0)

        self.__screen = pygame.display.get_surface()
        self.__screen.set_colorkey(color_key)

        pygame.display.set_caption(title)

        self.__blitted_boxes = []

        # Prepare the event system
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(allowed_events)

        # Prepare SDL-based clock system
        self.__clock = pygame.time.Clock()
        self.__max_fps = max_fps
        self.__use_busy_loop = use_busy_loop

    # Input and time
    def dt(self):
        """SDL.dt() -> time it took to render the last frame"""

        if self.__use_busy_loop:

            dt = self.__clock.tick_busy_loop(self.__max_fps)

        else:

            dt = self.__clock.tick(self.__max_fps)

        return dt

    def input(self):
        """SDL.input() -> an Event or None"""

        return pygame.event.poll()

    def update(self):
        """SDL.update()

        Call every iteration to ensure that drawing works properly -- in PyGame
        everything is first drawn to a buffer and only later, with this,
        applied on top of the display memory.
        """

        if self.__blitted_boxes:
            pygame.display.update(self.__blitted_boxes)
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

    # State
    def screen_size(self):
        """SDL.screen_size -> (width, height)"""

        return self.__screen.get_size()

    def fullscreen(self):
        """SDL.fullscreen() -> bool

        Tell whether the display is in fullscreen mode or not.
        """

        self.__internals.fullscreen()

    # Rendering and options
    def options(self):
        """SDL.options() -> an Options object

        Return an object used to set options from a Director.
        """

        return self.__opt

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
        coords = self.__to_screen_coords(Box(x,
                                             y,
                                             sprite.get_width(),
                                             sprite.get_height()),
                                         SCALE,
                                         viewport)

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
