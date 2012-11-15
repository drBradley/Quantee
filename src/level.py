# -*- coding: utf-8 -*-


__all__ = ['Level']


class Level(object):
    """Level class"""

    def __init__(self, stage, ender):

        self.__stage = stage
        self.__ender = ender

    # Game logic
    def step(self, dt, event):
        """L.step(dt, event) -> a Level or None

        Unless the level has finished, performs a logical step and
        returns itself. Otherwise -- returns a new level or None.
        """

        # If the level is done, return the next one
        if self.__ender.done(dt, event, self.__stage):

            return self.__ender.next_level()

        # Perform a logical game step
        for entity in self.__stage:
            entity.decide(dt, event, self.__stage)

        for entity in self.__stage:
            entity.act()

        self.__stage.harvest_dead()
        self.__stage.spawn()

        # Continue the current level
        return self

    # Rendering
    def viewport(self, engine):
        """L.viewport() -> a Box

        Returns the part of the level to be visible on screen."""

        raise NotImplementedError()

    def render(self, engine):
        """L.render(engine)

        Draw the visible part of the level on screen.
       """

        #engine.set_viewport(self.viewport(engine))

        # See which Entities need to be cleared, which need only to be
        # redrawn, and which need no action

        # Render the Entities in proprer order
