# -*- coding: utf-8 -*-

__all__ = ['Game']


class Game(object):
    """Base class for games."""

    def __init__(self, engine, init_level):

        self.__engine = engine

        self.__level = init_level

    def run(self):
        """G.run()

        Run the Game.
        """

        # Until the game stops, iterate over the events
        while self.__level is not None:

            event = self.__engine.input()

            # Perform a logical step of the game
            self.__level = self.__level.step(self,
                    self.__engine.dt(),
                    event,
                    self.__engine)

            # Render the level and calculate the next dt
            self.__level.render(self.__engine)

            self.__engine.tick()
