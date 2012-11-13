# -*- coding: utf-8 -*-


__all__ = ['Level']


class Level(object):
    """Level class"""

    def __init__(self, cam, stage, ender):

        self.__cam = cam
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
    def render(self, engine):
        """L.render(engine)

        Draw the visible part of the level on screen.
       """

        self.__stage.render(engine, self.__cam.viewport(self.__stage))
