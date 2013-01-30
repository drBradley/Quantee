# -*- coding: utf-8 -*-


import logging

__all__ = ['Level']


logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


class Level(object):
    """Level class"""

    def __init__(self, director, stage):

        logger.info("Level created")

        self.__director = director
        self.__stage = stage

    # Game logic
    def step(self, dt, event, levels, options):
        """L.step(dt, event, levels, options)

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

        self.__director.orchestrate(dt, event,
                                    self.__stage,
                                    levels,
                                    options)

    # Rendering
    def render(self, engine, strategy):
        """L.render(engine, strategy)

        Draw the visible part of the level on screen.
        """

        stage = self.__stage

        viewport = self.__director.viewport(stage)

        strategy.render(stage, engine, viewport)
