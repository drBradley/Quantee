# -*- coding: utf-8 -*-


from boxes import Box, collide

__all__ = ['Entity']


class State(object):
    """State() -> a state

    Helper class allowing the creation of arbitrary fields.
    """


class Entity(object):
    """Entity class, used to represent all in-game objects."""

    def __init__(self, pos, b_box, r_box, state, behaviour):

        # Initialise the fields
        self.__behaviour = behaviour

        self.__next = State()
        self.__curr = State()

        self.__needs_redraw = False
        self.__seen_if_others_need_redraw = False

        # Initialise the next and current state
        for ed in (self.__next, self.__curr):

            ed.dead = False
            ed.state = state

            ed.move = (0, 0)
            ed.v = (0, 0)

            x, y = pos
            ed.x = x
            ed.y = y

            ed.b_box = Box(x, y, *b_box)
            ed.r_box = Box(x, y, *r_box)

        self.__behaviour.prepare(self.__curr, self.__next)

    # Game logic
    @property
    def pos(self):
        """E.pos -> (x, y)"""

        return self.__curr.pos

    @property
    def b_box(self):
        """E.b_box -> Box(0, 0, w, h)"""

        return self.__curr.b_box

    @property
    def r_box(self):
        """E.r_box -> Box(0, 0, w_r, h_r)"""

        return self.__curr.r_box

    @property
    def move(self):
        """E.move -> (dx, dy)"""

        return self.__curr.move

    @property
    def v(self):
        """E.v -> (v_x, v_y)"""

        return self.__curr.v

    @property
    def state(self):
        """E.state -> name of sprite to use for rendering"""

        return self.__curr.state

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

    @property
    def dead(self):
        """E.dead -> True or False

        Tell whether the Entity is dead or alive. Dead Entities get
        harvested by the Level.
        """

        return self.__curr.dead

    # Rendering
    def force_redraw(self, viewport):
        """E.force_redraw(viewport)

        Forces the Entity to re-draw a part of itself in the next rendering
        pass.
        """

        if not self.__needs_redraw and collide(self.r_box, viewport):

            self.__needs_redraw = True

    def do_i_need_redraw(self, viewport):
        """E.do_i_need_redraw(viewport) -> True or False

        Check whether the Entity needs a re-draw because of her own change of
        state.
        """

        # If it has already been determined, than obviously, yes the Entitiy
        # needs to be redrawn
        if self.__needs_redraw:

            return True

        # First, check if the Entity is visible at all
        x, y = self.__curr.pos
        r_box = self.__curr.r_box

        r_box.move_by(x, y)

        visible_at_all = collide(r_box, viewport)

        r_box.move_by(-x, -y)

        # Check the other requirements for redrawing
        sprite_changed = self.__curr.state != self.__next.state

        position_changed = (self.__curr.x != self.__next.x or
                            self.__curr.y != self.__next.y)

        # Conclude the reasoning
        do_i = (sprite_changed or position_changed) and visible_at_all

        if do_i:
            self.force_redraw(viewport)

        return do_i

    def who_else_to_redraw(self, viewport):
        """E.who_else_to_redraw(viewport) -> a set

        The Entities that will need redrawing if the current one will.
        """

        collides = self.__curr.collisions
        collided = self.__next.collisions

        who_else = collides.symmetric_difference(collided)

        if self.__needs_redraw and self.__seen_if_others_need_redraw:

            for other in who_else:
                other.force_redraw(viewport)
                other.who_else_to_redraw(viewport)

            self.__seen_if_others_need_redraw = True

        return who_else

    def draw(self, engine, viewport):
        """E.draw(engine, viewport)

        Given an Engine and a Box describing the viewport, draws the parts of
        itself that need refreshing.
        """

        # FIXME: Implement drawing

        self.__needs_redraw = False
        self.__seen_if_others_need_redraw = False
