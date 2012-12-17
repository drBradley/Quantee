# -*- coding: utf-8 -*-

__all__ = ['Game']


class Game(object):
    """Base class for games."""

    def __init__(self, engine, init_level, timestep=1000 / 60,
                 max_steps_per_render=100):

        self.__engine = engine

        self.__timestep = timestep
        self.__max_steps_per_render = max_steps_per_render

        self.__levels = [init_level]

    def run(self):
        """G.run()

        Run the Game.
        """

        # Prepare for time-handling
        max_steps_per_render = self.__max_steps_per_render
        timestep = self.__timestep
        time_left = 0

        # Until the game stops, iterate over the events
        while len(self.__levels) > 0:

            # Render the level and get the render time
            self.__levels[-1].render(self.__engine)

            dt = self.__engine.dt()

            # Perform enough logical steps of the game to cover the rendering
            # time
            time_left += dt
            steps = 0

            while time_left >= dt and steps < max_steps_per_render:

                event = self.__engine.input()

                self.__levels[-1].step(
                    timestep,
                    event,
                    self.__levels)

                steps += 1
                time_left -= timestep

            print "%d physics steps performed" % steps

            # Let the engine do whatever it needs to
            self.__engine.update()
