# -*- coding: utf-8 -*-


import logging

__all__ = ['Game']


logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


class Game(object):
    """Base class for games."""

    def __init__(self, engine, drawing_strategy, init_level, timestep=1000 /
                 60, max_steps_per_render=100):

        self.__engine = engine
        self.__drawing_strategy = drawing_strategy

        self.__timestep = timestep
        self.__max_steps_per_render = max_steps_per_render

        self.__levels = [init_level]

        logger.info('Game created')
        logger.info('Steps per render limited to %d', max_steps_per_render)
        logger.info('Physics time step is %d', timestep)

    def __levels_left(self):

        left = len(self.__levels)

        logger.debug('There are %d levels left in the level stack', left)

        return left

    def run(self):
        """G.run()

        Run the Game.
        """

        # Prepare for time-handling
        max_steps_per_render = self.__max_steps_per_render
        timestep = self.__timestep
        time_left = 0

        # Until the game stops, iterate over the events
        while self.__levels_left():

            # Render the level and get the render time
            if self.__engine.options().screen_changed():

                logger.warning('Deprecated! Forcing redraw of all Entities '
                               'after resolution change')

                self.__drawing_strategy.force_all()

            logger.info('Drawing a frame')

            self.__levels[-1].render(
                self.__engine,
                self.__drawing_strategy)

            dt = self.__engine.dt()

            logger.info('The render time was %f', dt)

            # Perform enough logical steps of the game to cover the rendering
            # time
            time_left += dt
            steps = 0

            logger.info('The time accumulator is %f', time_left)

            while (time_left >= dt and
                   steps < max_steps_per_render):

                # When no levels are left, just exhaust the time left without
                # advancing anything
                if self.__levels_left():

                    event = self.__engine.input()

                    logger.info('Performing physics steps')

                    self.__levels[-1].step(
                        timestep,
                        event,
                        self.__levels,
                        self.__engine.options())

                    steps += 1

                time_left -= timestep

            # Let the engine do whatever it needs to
            logger.info('Calling the Engine\'s update method')

            self.__engine.update()
