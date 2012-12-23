# -*- coding: utf-8 -*-


__all__ = ['Level']


class Level(object):
    """Level class"""

    def __init__(self, director, stage):

        self.__director = director
        self.__stage = stage

    # Game logic
    def step(self, dt, event, levels):
        """L.step(dt, event, levels)

        Performs a logical step.
        """

        for entity in self.__stage:

            entity.decide(dt, event,
                          self.__stage,
                          self.__director.hints(entity))

        for entity in self.__stage:

            entity.act()

        self.__stage.harvest_dead()
        self.__stage.spawn()

        self.__director.orchestrate(dt, event, self.__stage, levels)

    # Rendering
    def render(self, engine, strategy):
        """L.render(engine, strategy)

        Draw the visible part of the level on screen.
        """

        stage = self.__stage

        viewport = self.__director.viewport(stage)

        strategy.render(stage, engine, viewport)
