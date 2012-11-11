# -*- coding: utf-8 -*-


from boxes import Box

__all__ = ['Entity']


class State(object):
    """Helper class allowing the creation of arbitrary fields."""


class Entity(object):
    """Entity class, used to represent all in-game objects."""

    def __init__(self, pos, b_box, r_box, behaviour):

        # Initialise the fields
        self.__behaviour = behaviour

        self.__next = State()
        self.__curr = State()

        # Initialise the next and current state
        for ed in [self.__next, self.__curr]:

            ed.dead = False

            x, y = ed.pos = pos

            ed.move = (0, 0)
            ed.v = (0, 0)

            ed.b_box = Box(x, y, *b_box)
            ed.r_box = Box(x, y, *r_box)

            self.__behaviour.prepare(ed)

    # Game logic
    @property
    def pos(self):
        """E.pos -> (x, y)"""

        return self.__curr.pos

    @property
    def move(self):
        """E.move -> (dx, dy)"""

        return self.__curr.move

    @property
    def v(self):
        """E.v -> (v_x, v_y)"""

        return self.__curr.v

    def decide(self, dt, event, level):
        """E.decide(dt, event, level)

        Decide what to do in the current step.
        """

        self.__behaviour.decide(dt, event, level,
                self.__curr, self.__next)

    def act(self):
        """E.act()

        Execute the actions chosen upon the last call to decide.
        """

        self.__next, self.__curr = self.__curr, self.__next

    @property
    def dead(self):
        """E.dead -> True or False

        Tell whether the Entity is dead or alive. Dead Entities get
        harvested by the Level.
        """

        return self.__curr.dead

    # Rendering
    def draw(self, engine):
        """E.draw(engine)

        Given an Engine, draws itself.
        """

        raise NotImplementedError()
