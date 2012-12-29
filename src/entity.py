# -*- coding: utf-8 -*-


from boxes import Box, collide

__all__ = ['Entity']


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

        self.__was_drawn = False

        x, y = pos

        # Initialise the next and current state
        for st in (self.__next, self.__curr, self.__prev):

            st.dead = False
            st.state = state

            st.v = (0, 0)

            st.b_box = Box(x, y, *b_box)
            st.r_box = Box(x, y, *r_box)

        self.__behaviour.prepare(self.__prev, self.__curr, self.__next)

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
    def decide(self, dt, event, stage):
        """E.decide(dt, event, stage)

        Decide what to do in the current step.
        """

        self.__behaviour.decide(
            dt, event,
            stage,
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
    def was_drawn(self):

        return self.__was_drawn

    def draw(self, engine, viewport):
        """E.draw(engine, viewport)

        Given an Engine and a Box describing the viewport, draws the parts of
        itself that need refreshing.
        """

        r_box = self.present().r_box()

        pos = (r_box.x, r_box.y)

        engine.draw(
            pos,
            self.present().state_name(),
            viewport)

        self.__was_drawn = True
