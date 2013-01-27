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

    def __init__(self, g, a_jump, a_run, a_fall, drag, friction,
                 starts_on_ground=False):

        self.__g = g
        self.__a_jump = a_jump
        self.__a_run = a_run
        self.__a_fall = a_fall

        self.__drag = drag
        self.__friction = friction

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

    def run(self, dt, event):
        """JNR.run(dt, event)

        Alter the velocity's horizontal component.
        """

        accel = self.__a_run if self.__on_ground else self.__a_fall
        decel = self.__friction if self.__on_ground else self.__drag

        vx, vy = self.__v

        if event.left_is_down():

            vx -= accel * dt

        elif event.right_is_down():

            vx += accel * dt

        else:

            sign = math.copysign(1, vx)

            vx -= sign * min(decel * dt, abs(vx))

        self.__v = (vx, vy)

    def jump(self, dt, event):
        """JNR.jump(dt, event)

        Apply an impulse force if the jump button was pressed and the character
        is on ground.
        """

        a_jump = self.__a_jump

        vx, vy = self.__v

        if event.jump_pressed() and self.__on_ground:

            print "Jump!"

            print "vy = %f\ta_jump = %f\tdt = %f" % (vy, a_jump, dt)

            vy += a_jump * dt

            print "vy' = %f" % vy

            self.__on_ground = False

        self.__v = (vx, vy)

    def handle_ground_collision(self, dt, obox, box):
        """JNR.handle_ground_collision(dt, obox, box)

        Ensure the character doesn't fall through the ground.
        """

        vx, vy = self.__v

        dx = vx * dt
        dy = vy * dt

        if box.y + dy <= obox.y + obox.h <= box.y and\
                (obox.x <= box.x + dx <= obox.x + obox.w or
                    obox.x <= box.x + box.w + dx <= obox.x + obox.w):

            ground = obox.y + obox.h

            dy = max(dy, ground - box.y)

            self.__on_ground = True

        vy = dy / dt

        self.__v = (vx, vy)

    def handle_wall_collision(self, dt, obox, box):
        """JNR.handle_wall_collision(dt, obox, box)

        Keep the character from passing through walls.
        """

        vx, vy = self.__v

        dx = vx * dt
        dy = vy * dt

        hits_wall_on_left = box.x + dx <= obox.x + obox.w <= box.x
        hits_wall_on_right = box.x + box.w < obox.x <= box.x + box.w + dx

        y_matches = (
            obox.y <= box.y + dy <= obox.y + obox.h or
            obox.y <= box.y + box.h + dy <= obox.y + obox.h)

        if hits_wall_on_left and y_matches:

            dx = max(dx, obox.x + obox.w - box.x)

        elif hits_wall_on_right and y_matches:

            dx = min(dx, obox.x - box.x - box.w - 1)
            # TODO: Figure out why the following is necessary
            dx = max(dx, 0)  # prevent bouncing off the wall

        vx = dx / dt

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

        # Apply forces
        self.freefall(dt)

        self.run(dt, event)

        self.jump(dt, event)

        # Handle collisions
        self.__on_ground = False

        for entity in stage:

            if isinstance(entity, Environment) and entity.is_obstacle():

                self.handle_ground_collision(
                    dt,
                    entity.present().b_box(),
                    curr.b_box)

                self.handle_wall_collision(
                    dt,
                    entity.present().b_box(),
                    curr.b_box)

        # Move the character
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
            JumpNRun(-1e-3, 3e-2, 1e-4, 1e-5, 5e-5, 5e-4))


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

    def __init__(self, box, star, toggle_fullscreen_each_s=15):

        self.__box = box

        self.__star = star
        self.__collected = False

    def empty(self, levels):
        """DD.empty(levels)

        Empty the levels stack.
        """

        for i in range(len(levels)):

            levels.pop()

    def show_win_message(self, stage):
        """DD.show_win_message(stage)

        Shows the win message onscreen.
        """

        w, h = 597, 286

        x, y = 800 - 60 - w, 120

        win_message = Environment(
            x, y,
            (w, h),
            'win_screen')

        stage.add_spawn(win_message, 'overlay')

    def handle_star_collection(self, event, stage, levels):
        """DD.handle_star_collection(event, stage, levels)

        Deals with the collection of a star and game restarting.
        """

        if not self.__collected:

            collected = True

            for entity in stage:

                if entity is self.__star:

                    collected = False

            self.__collected = collected

            if collected:

                    self.show_win_message(stage)

        else:

            if event.jump_pressed():

                self.empty(levels)

                levels.append(DumbLevel())

    def hints(self, entity):

        return None

    def orchestrate(self, dt, event, stage, levels, options):

        if event.quit() or event.escape():

            self.empty(levels)

        self.handle_star_collection(event, stage, levels)

    def viewport(self, stage):

        return self.__box


class DumbLevel(Level):
    """DumbLevel() -> a dumb Level

    It is empty and will end only on a QUIT event, and end the game
    alltogether.
    """

    def __init__(self):

        # Get a cam and a stage
        stage = Stage((800, 600), ['bg', 'movers', 'overlay'], 'movers')

        star = Star(710, 30)

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

        stage.add_spawn(Environment(30, 150,
                                    (60, 60),
                                    'sqr', True),
                        'bg')

        stage.add_spawn(star)

        stage.add_spawn(Psi(35, 100))

        stage.spawn()

        # Call the superclasses initialiser
        super(DumbLevel, self).__init__(
            DumbDirector(Box(0, 0, 800, 600), star),
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
