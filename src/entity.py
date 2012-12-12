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

        self.__needs_redraw = True
        self.__seen_if_others_need_redraw = False

        # Initialise the next and current state
        for st in (self.__next, self.__curr):

            st.dead = False
            st.state = state

            st.move = (0, 0)
            st.v = (0, 0)

            x, y = pos
            st.x = x
            st.y = y

            st.b_box = Box(x, y, *b_box)
            st.r_box = Box(x, y, *r_box)

            st.collisions = set()

        self.__behaviour.prepare(self.__curr, self.__next)

    # Behaviour
    def decide(self, dt, event, stage):
        """E.decide(dt, event, stage)

        Decide what to do in the current step.
        """

        self.__behaviour.decide(
            dt, event,
            stage,
            self.__curr, self.__next)

    def act(self):
        """E.act()

        Execute the actions chosen upon the last call to decide.
        """

        self.__next, self.__curr = self.__curr, self.__next

    # Rendering
    def needs_redraw(self, viewport, others=set()):
        """E.needs_redraw(viewport[, others])

        See if the entity needs to be redrawn. The optional argument others is
        a set of other entities which do need to be redrawn -- if something
        colliding with the current one does, so does it.
        """

        if collide(self.__next.r_box, viewport):
            return True

        return False

    def draw(self, engine, viewport):
        """E.draw(engine, viewport)

        Given an Engine and a Box describing the viewport, draws the parts of
        itself that need refreshing.
        """

        engine.draw(
            self.pos,
            self.state,
            viewport)
