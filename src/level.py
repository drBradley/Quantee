# -*- coding: utf-8 -*-


__all__ = ['Level']


class Level(object):
    """Level class"""

    def __init__(self, cam, stage, ender):

        self.__cam = cam
        self.__stage = stage
        self.__ender = ender

    # Game logic
    def step(self, dt, event, levels):
        """L.step(dt, event, levels)

        Performs a logical step.
        """

        if not self.__ender.done(dt, event, self.__stage, levels):

            for entity in self.__stage:
                entity.decide(dt, event, self.__stage)

            for entity in self.__stage:
                entity.act()

            self.__stage.harvest_dead()
            self.__stage.spawn()

    # Rendering
    def render(self, engine):
        """L.render(engine)

        Draw the visible part of the level on screen.
        """

        self.__stage.render(engine, self.__cam.viewport(self.__stage))
