# -*- coding: utf-8 -*-

import os.path
import math

import pygame

from game import Game
from level import Level
from drawing_strategy import Everyone
from stage import Stage
from ender import Ender
from entity import Entity
from behaviour import Behaviour
from boxes import Box

from cam import StaticCam
from assets import QAssets
from sdl import SDL, EventManager


class DoNothing(Behaviour):
    """DoNothing() -> a Behaviour for static objects"""

    def prepare(self, prev, curr, next):
        pass

    def decide(self, dt, event, stage, prev, curr, next):
        pass


class Background(Entity):
    """Background(image_name) -> a still background image"""

    def __init__(self, x, y, image_name):

        super(Background, self).__init__(
            (x, y),
            (400, 400),
            (400, 400),
            image_name,
            DoNothing())


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

    def decide(self, dt, events, stage, prev, curr, next):

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


class SquareMover(Entity):

    def __init__(self, sprite_name, points, die_after=None):

        super(SquareMover, self).__init__(
            (200, 100),
            (30, 30),
            (30, 30),
            sprite_name,
            MoveOverPath(.1, points, die_after))


class DumbEnder(Ender):
    """DumbEnder() -> a dumb Ender

    Ends the whole game when the window is closed or ESC is pressed.
    """

    def done(self, dt, event, stage, levels):

        if (event is not None and
                (event.type == pygame.QUIT or

                (event.type == pygame.KEYDOWN and
                 event.key == pygame.K_ESCAPE))):

            for i in range(len(levels)):
                levels.pop()

            return True

        return False


class DumbLevel(Level):
    """DumbLevel() -> a dumb Level

    It is empty and will end only on a QUIT event, and end the game
    alltogether.
    """

    def __init__(self):

        # Get a cam and a stage
        cam = StaticCam(Box(0, 0, 640, 480))
        stage = Stage((400, 400), ['bg', 'movers'], 'movers')

        # Spawn the entities
        stage.add_spawn(Background(0, 0, 'bg'), 'bg')

        stage.add_spawn(Background(410, 410, 'bg'), 'bg')

        stage.add_spawn(SquareMover('red_box', [
            (100, 100),
            (100, 300),
            (300, 300),
            (300, 100)],
            150))

        stage.add_spawn(SquareMover('green_box', [
            (200, 10),
            (10, 200),
            (200, 200)]))

        stage.spawn()

        # Call the superclasses initialiser
        super(DumbLevel, self).__init__(cam, stage, DumbEnder())


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
                     (640, 480),
                     QAssets(asset_path),
                     DumbManager(),
                     max_fps=32)

        strategy = Everyone()

        init_level = DumbLevel()

        super(QuanteeTheGame, self).__init__(
            engine,
            strategy,
            init_level)


if __name__ == '__main__':
    game = QuanteeTheGame()
    game.run()
