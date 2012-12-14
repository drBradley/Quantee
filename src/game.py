# -*- coding: utf-8 -*-

__all__ = ['Game']


class Game(object):
    """Base class for games."""

    def __init__(self, engine, init_level):

        self.__engine = engine

        self.__levels = [init_level]

    def run(self):
        """G.run()

        Run the Game.
        """

        # Until the game stops, iterate over the events
        while len(self.__levels) > 0:

            # Render the level and get new input
            self.__levels[-1].render(self.__engine)

            event, dt = self.__engine.input()

            # Perform a logical step of the game
            self.__levels[-1].step(
                dt,
                event,
                self.__levels)

            # Let the engine do whatever it needs to
            self.__engine.update()
