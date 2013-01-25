# -*- coding: utf-8 -*-

import os.path
import math

from game import Game
from level import Level
from drawing_strategy import DirtyWholes
from stage import Stage
from director import Director
from entity import Entity
from behaviour import Behaviour
from boxes import Box, collide

from assets import QAssets
from qengine import QEngine


class DoNothing(Behaviour):
    """DoNothing() -> a Behaviour for static objects"""

    def prepare(self, prev, curr, next):
        pass

    def decide(self, dt, event, stage, hint, prev, curr, next):
        pass


class Environment(Entity):
    """Environment(x, y, (w, h), image_name[, is_obstacle]) -> a still image"""

    def __init__(self, x, y, size, image_name, is_obstacle=False):

        super(Environment, self).__init__(
            (x, y),
            size,
            size,
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


class JumpNRun(Behaviour):

    def __init__(self, g, a_run, v_stop, v_max, starts_on_ground=False):

        self.__g = g

        self.__a_run = a_run
        self.__v_stop = v_stop

        self.__v_max = v_max

        self.__v = (0, 0)
        self.__on_ground = starts_on_ground

    def prepare(self, prev, curr, next):

        pass

    def freefall(self, dt):
        """JNR.freefall(dt)

        Makes the Entity fall down with the set gravitational acceleration
        unless it touches the ground.
        """

        g = self.__g
        vx, vy = self.__v

        if not self.__on_ground:

            vy += g * dt

        else:

            vy = 0

        self.__v = (vx, vy)

    def run_accel(self, dt, event):
        """JNR.run_accel(dt, event)

        Alter the velocity's horizontal component.
        """

        a_run = self.__a_run
        #v_stop = self.__v_stop

        vx, vy = self.__v

        if event.left_is_down():
            vx -= a_run * dt

        elif event.right_is_down():
            vx += a_run * dt

        else:

            vx = 0

        self.__v = (vx, vy)

    def limit_speed(self, dt):
        """JNR.limit_speed(st)

        Ensure the speed doesn't cross the maximum set.
        """

        v_max = self.__v_max
        vx, vy = self.__v

        v_norm = math.sqrt(vx ** 2 + vy ** 2)

        if v_norm > v_max:

            vx *= v_max / v_norm
            vy *= v_max / v_norm

        self.__v = (vx, vy)

    def handle_ground_collision(self, dt, stage, box):
        """JNR.handle_ground_collision(dt, stage, box)

        Ensure the character doesn't fall through the ground.
        """

        vx, vy = self.__v

        dx = vx * dt
        dy = vy * dt

        dys = []

        for entity in stage:

            # And would collide with an obstacle
            if isinstance(entity, Environment) and entity.is_obstacle():

                obox = entity.present().b_box()

                # Don't allow it to fall through
                if box.y + dy <= obox.y + obox.h <= box.y and\
                        (obox.x <= box.x + dx <= obox.x + obox.w or
                         obox.x <= box.x + box.h + dx <= obox.x + obox.w):

                    ground = obox.y + obox.h

                    dys.append(ground - box.y)

        if dys:

            vy = min(dys) / dt

        self.__v = (vx, vy)

    def move(self, dx, dy, curr, next):
        """JNR.move(dx, dy, curr, next)

        Move the entity by (dx, dy).
        """

        for box, pbox in [(next.b_box, curr.b_box),
                          (next.r_box, curr.r_box)]:

            box.move_to(pbox.x, pbox.y)
            box.move_by(dx, dy)

    def decide(self, dt, event, stage, hint, prev, curr, next):

        self.freefall(dt)

        self.run_accel(dt, event)

        self.limit_speed(dt)

        if not self.__on_ground:

            self.handle_ground_collision(dt, stage, curr.b_box)

        vx, vy = self.__v

        dx = vx * dt
        dy = vy * dt

        self.move(dx, dy, curr, next)


class Psi(Entity):
    """Psi(x, y) -> Psi, the quantum boy"""

    def __init__(self, x, y):

        super(Psi, self).__init__(
            (x, y),
            (40, 50),
            (40, 50),
            'psi',
            JumpNRun(-1e-3, 1e-4, 0.05, 0.1))


class Star(Entity):
    """Star(x, y) -> a collectible star"""

    def __init__(self, x, y):

        super(Star, self).__init__(
            (x, y),
            (63, 63),
            (60, 60),
            "star",
            GetCollected(Psi))


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

    def hints(self, entity):

        return None

    def orchestrate(self, dt, event, stage, levels, options):

        # Close the game when the window gets closed or the player presses
        # Escape
        if event.quit() or event.escape():

            for i in range(len(levels)):
                levels.pop()

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
        stage.add_spawn(Environment(30, 30,
                                    (740, 540),
                                    'bg'),
                        'bg')

        stage.add_spawn(Environment(0, 0,
                                    (800, 30),
                                    'h_bar', True),
                        'bg')

        stage.add_spawn(Environment(0, 570,
                                    (800, 30),
                                    'h_bar', True),
                        'bg')

        stage.add_spawn(Environment(0, 30,
                                    (30, 540),
                                    'v_bar', True),
                        'bg')

        stage.add_spawn(Environment(770, 30,
                                    (30, 540),
                                    'v_bar', True),
                        'bg')

        stage.add_spawn(Environment(370, 30,
                                    (60, 60),
                                    'sqr', True),
                        'bg')

        stage.add_spawn(Environment(30, 30,
                                    (60, 60),
                                    'sqr', True),
                        'bg')

        stage.add_spawn(Star(710, 30))

        stage.add_spawn(Psi(35, 300))

        stage.spawn()

        # Call the superclasses initialiser
        super(DumbLevel, self).__init__(
            DumbDirector(Box(0, 0, 800, 600)),
            stage)


class QuanteeTheGame(Game):
    """QuanteeTheGame() -> our game"""

    def __init__(self):

        asset_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            'assets')

        color_key = (255, 0, 255)

        sdl = QEngine("Quantee",
                      (800, 600),
                      color_key,
                      QAssets(color_key, asset_path),
                      max_fps=32)

        strategy = DirtyWholes()

        init_level = DumbLevel()

        super(QuanteeTheGame, self).__init__(
            sdl,
            strategy,
            init_level)


if __name__ == '__main__':
    game = QuanteeTheGame()
    game.run()
