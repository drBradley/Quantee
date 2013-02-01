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
