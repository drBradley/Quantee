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
            level = self.__levels[-1].step(
                    dt,
                    event)

            if level is None:
                self.__levels.pop()

            elif level is not self.__levels[-1]:
                self.__levels.append(level)

            # Tick the game clock
            self.__engine.tick()
