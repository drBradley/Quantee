# -*- coding: utf-8 -*-


__all__ = ['Level']


class Level(object):
    """Level class"""

    def __init__(self, container, ender):
        pass

    @property
    def entities(self):
        """L.entities

        An iterator over the Entities in the Level. The Entities are to
        be in the rendering order.
        """

        raise NotImplementedError()

    # Game logic
    def step(self, dt, event):
        """L.step(dt, event) -> a Level or None

        Unless the level has finished, performs a logical step and
        returns itself. Otherwise -- returns a new level or None.
        """

        # If the level is done, return the next one
        if self.done:

            return self.next_level

        # Perform a logical game step
        for entity in self.entities:
            entity.decide(dt, event, self)

        for entity in self.entities:
            entity.act()

        self.harvest_dead()

        # Continue the current level
        return self

    def harvest_dead(self):
        """L.harvest_dead()

        Get rid of the dead Entities.
        """

        raise NotImplementedError()

    @property
    def done(self):
        """L.done -> True or False

        Has the level finished?
        """

        raise NotImplementedError()

    @property
    def next_level(self):
        """L.next_level -> another Level or None

        The level to follow the current one. The value may be
        undefined untill L.done is True.
        """

        raise NotImplementedError()

    # Rendering
    def viewport(self, engine):
        """L.viewport() -> a Box

        Returns the part of the level to be visible on screen."""

        raise NotImplementedError()

    def render(self, engine):
        """L.render(engine)

        Draw the visible part of the level on screen.
       """

        engine.set_viewport(self.viewport(engine))

        # See which Entities need to be cleared, which need only to be
        # redrawn, and which need no action

        # Render the Entities in proprer order
