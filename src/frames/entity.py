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


import logging

from boxes import Box

__all__ = ['Entity']


logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


class State(object):
    """State() -> a state

    Helper class allowing the creation of arbitrary fields.
    """


class StateWrapper(object):
    """StateWrapper(State) -> a state wrapper

    Used to expose only a subset of a State's fields.
    """

    def __init__(self, state):

        self.__state = state

    def b_box(self):

        return self.__state.b_box

    def r_box(self):

        return self.__state.r_box

    def v(self):

        return self.__state.v

    def state_name(self):

        return self.__state.state

    def dead(self):

        return self.__state.dead


class Entity(object):
    """Entity class, used to represent all in-game objects."""

    def __init__(self, pos, b_box, r_box, state, behaviour,
                 wrapper=StateWrapper):

        # Initialise the fields
        self.__behaviour = behaviour

        self.__next = State()
        self.__curr = State()
        self.__prev = State()

        self.__next_wrap = StateWrapper(self.__next)
        self.__curr_wrap = StateWrapper(self.__curr)
        self.__prev_wrap = StateWrapper(self.__prev)

        x, y = pos

        # Initialise the next and current state
        for st in (self.__next, self.__curr, self.__prev):

            st.dead = False
            st.state = state

            st.v = (0, 0)

            st.b_box = Box(x, y, *b_box)
            st.r_box = Box(x, y, *r_box)

        self.__behaviour.prepare(self.__prev, self.__curr, self.__next)

        logger.info(
            '%s driven by %s created',
            self.__class__.__name__,
            self.__behaviour.__class__.__name__)

    # State exposers
    def present(self):
        """E.present() -> a StateWrapper

        Returns an object giving access to the current state of the Entity
        through getters.
        """

        return self.__curr_wrap

    def past(self):
        """E.past() -> a StateWrapper

        Returns an object giving access to the previous state of the Entity
        through getters.
        """

        return self.__prev_wrap

    # Behaviour
    def decide(self, dt, event, stage, hint):
        """E.decide(dt, event, stage, hint)

        Decide what to do in the current step.
        """

        self.__behaviour.decide(
            dt, event,
            stage, hint,
            self.__prev, self.__curr, self.__next)

    def act(self):
        """E.act()

        Execute the actions chosen upon the last call to decide.
        """

        self.__next, self.__curr, self.__prev = (
            self.__prev,
            self.__next,
            self.__curr)

        self.__next_wrap, self.__curr_wrap, self.__prev_wrap = (
            self.__prev_wrap,
            self.__next_wrap,
            self.__curr_wrap)

    # Rendering
    def draw(self, engine, viewport):
        """E.draw(engine, viewport)

        Given an Engine and a Box describing the viewport, draws itself.
        """

        r_box = self.present().r_box()

        pos = (r_box.x, r_box.y)

        engine.draw(
            pos,
            self.present().state_name(),
            viewport)

        self.__was_drawn = True
