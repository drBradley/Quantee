# -*- coding: utf-8 -*-

import os.path
import math

import pygame

from game import Game
from level import Level
from drawing_strategy import DirtyWholes
from stage import Stage
from director import Director
from entity import Entity
from behaviour import Behaviour
from boxes import Box, collide

from assets import QAssets
from sdl import SDL, EventManager


class DoNothing(Behaviour):
    """DoNothing() -> a Behaviour for static objects"""

    def prepare(self, prev, curr, next):
        pass

    def decide(self, dt, event, stage, hint, prev, curr, next):
        pass


class Environment(Entity):
    """Environment(x, y, image_name[, is_obstacle]) -> a still image"""

    def __init__(self, x, y, image_name, is_obstacle=False):

        super(Environment, self).__init__(
            (x, y),
            (400, 400),
            (400, 400),
            image_name,
            DoNothing())

        self.__is_obstacle = is_obstacle

    def is_obstacle(self):
        """E.is_obstacle() -> bool"""

        return self.__is_obstacle


class GetCollected(Behaviour):
    """GetCollected(cls) -> a Behaviour which kills it's Entity one physics
    step after colliding with any entity of type cls
    """

    def __init__(self, cls):

        self.__cls = cls

    def prepare(self, prev, curr, next):
        pass

    def decide(self, dt, event, stage, hint, prev, curr, next):

        if curr.dead:

            next.dead = True

        for entity in stage:

            if isinstance(entity, self.__cls) and\
                    collide(curr.b_box, entity.present().b_box()):

                next.dead = True


class MoveOverPath(Behaviour):
    """MoveOverPath(speed, points) -> a Behaviour for objects following a path
    and moving with a constant speed
    """

    def __init__(self, speed, points, die_after=None):

        self.__speed = speed
        self.__points = points
        self.__heading_to = 0
        self.__die_after = die_after

    def prepare(self, prev, curr, next):

        die_after = self.__die_after

        prev.passed = die_after
        curr.passed = die_after - 1 if die_after is not None else die_after
        next.passed = die_after - 1 if die_after is not None else die_after

    def decide(self, dt, events, stage, hint, prev, curr, next):

        # Calculate the next position
        s = self.__speed
        x, y = curr.b_box.x, curr.b_box.y
        p, q = self.__points[self.__heading_to]

        v_x = s * math.copysign(1, p - x)
        v_y = s * math.copysign(1, q - y)

        x += dt * v_x
        y += dt * v_y

        next.b_box.move_to(x, y)
        next.r_box.move_to(x, y)

        # Turn, if close enough to the current crosshair point
        if abs(x - p) <= s * dt and abs(y - q) <= s * dt:

            if self.__heading_to + 1 < len(self.__points):

                self.__heading_to += 1

            else:

                self.__heading_to = 0

        # Die if an aproriate amount of steps has passed
        if curr.passed is not None:

            if curr.passed == 0:
                next.dead = True

            else:
                next.passed = curr.passed - 1


class DumbDirector(Director):
    """DumbDirector() -> a dumb Director

    Ends the whole game when the window is closed or ESC is pressed.

    Keeps the camera still.

    Gives no hints to Entities.
    """

    def __init__(self, box, toggle_fullscreen_each_s=15):

        self.__box = box

        self.__toggle_fullscreen_each_ms = toggle_fullscreen_each_s * 1000
        self.__time = 0
        self.__last_toggle = 0

    def hints(self, entity):

        return None

    def orchestrate(self, dt, event, stage, levels, options):

        # Close the game when the window gets closed or the player presses
        # Escape
        if (event is not None and
                (event.type == pygame.QUIT or

                (event.type == pygame.KEYDOWN and
                 event.key == pygame.K_ESCAPE))):

            for i in range(len(levels)):
                levels.pop()

        # Handle toggling between fullscreen and windowed mode each n seconds
        self.__time += dt

        toggle_no = self.__time / self.__toggle_fullscreen_each_ms

        if toggle_no > self.__last_toggle:

            options.set_fullscreen(bool(toggle_no % 2))
            options.confirm()

            self.__last_toggle += 1

    def viewport(self, stage):

        return self.__box


class DumbLevel(Level):
    """DumbLevel() -> a dumb Level

    It is empty and will end only on a QUIT event, and end the game
    alltogether.
    """

    def __init__(self):

        # Get a cam and a stage
        stage = Stage((800, 600), ['bg', 'movers'], 'movers')

        # Spawn the entities
        stage.add_spawn(Environment(0, 0, 'bg'), 'bg')

        stage.add_spawn(Environment(410, 410, 'bg'), 'bg')



        stage.spawn()

        # Call the superclasses initialiser
        super(DumbLevel, self).__init__(
            DumbDirector(Box(0, 0, 800, 600)),
            stage)


class DumbManager(EventManager):
    """DumbManager() -> a dumb EventManager

    It allows for the presence of QUIT, NOEVENT and KEYDOWN pygame events and
    passes them on unmodified.
    """

    __allowed = [
        pygame.QUIT,
        pygame.NOEVENT,
        pygame.KEYDOWN]

    @property
    def allowed(self):
        """DM.allowed -> list of allowed PyGame event types

        Contains pygame.QUIT and pygame.NOEVENT.
        """

        return self.__allowed

    def transform(self, raw_event):
        """DM.transform(raw_event) -> raw_event

        Performs no transformations.
        """

        return raw_event


class QuanteeTheGame(Game):
    """QuanteeTheGame() -> our game"""

    def __init__(self):

        asset_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            'assets')

        engine = SDL("Quantee",
                     (800, 600),
                     QAssets(asset_path),
                     DumbManager(),
                     max_fps=32)

        strategy = DirtyWholes()

        init_level = DumbLevel()

        super(QuanteeTheGame, self).__init__(
            engine,
            strategy,
            init_level)


if __name__ == '__main__':
    game = QuanteeTheGame()
    game.run()
