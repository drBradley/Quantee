# -*- coding: utf-8 -*-

# Copyright 2012-2013 Karol Marcjan and Bartosz Boguniewicz
#
# This file is part of Quantee.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

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
        self.__time_left = 0

        self.__levels = [init_level]

        logger.info('Game created')
        logger.info('Steps per render limited to %d', max_steps_per_render)
        logger.info('Physics time step is %d', timestep)

    def __levels_left(self):

        left = len(self.__levels)

        logger.debug('There are %d levels left in the level stack', left)

        return left

    def step_physics(self):
        """G.step_physics()

        Advances logical game time.
        """

        event = self.__engine.input()

        logger.info('Performing physics steps')

        self.__levels[-1].step(
            self.__timestep,
            event,
            self.__levels,
            self.__engine.options())

        self.__steps_in_frame += 1

        self.__time_left -= self.__timestep

    def multistep_physics(self):
        """G.multistep_physics()


        Perform enough logical steps of the game to cover the rendering time.

        Stops 'early' if no more levels are left after one of the steps.
        """

        self.__steps_in_frame = 0

        logger.info('The time accumulator is %f', self.__time_left)

        while (self.__time_left >= self.__last_frame and
                self.__steps_in_frame < self.__max_steps_per_render and
                self.__levels_left()):

                self.step_physics()

    def render(self):
        """G.render()

        Renders the current level.
        """

        logger.info('Drawing a frame')

        self.__levels[-1].render(
            self.__engine,
            self.__drawing_strategy)

        self.__last_frame = self.__engine.dt()
        self.__time_left += self.__last_frame

        logger.info('The render time was %f', self.__last_frame)

    def run(self):
        """G.run()

        Run the Game.
        """

        # Prepare for time-handling
        self.__time_left = 0

        # Until the game stops, iterate over the events
        while self.__levels_left():

            # When resolutions change everything is dirty
            if self.__engine.options().screen_changed():

                logger.warning('Deprecated! Forcing redraw of all Entities '
                               'after resolution change')

                self.__drawing_strategy.force_all()

            # Render the level and get the render time
            self.render()

            # Make as many physic steps as necessary
            self.multistep_physics()

            # Let the engine do whatever it needs to
            logger.info('Calling the Engine\'s update method')

            self.__engine.update()
