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

import pygame

from sdl import SDL


__all__ = ['QEngine']


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


down = dict(left=False,
            right=False)


class Event(object):
    """Wrapper for raw SDL events used in QTG"""

    def __init__(self, raw):

        if raw.type == pygame.KEYDOWN:

            if raw.key == pygame.K_LEFT:

                down['left'] = True

            elif raw.key == pygame.K_RIGHT:

                down['right'] = True

        elif raw.type == pygame.KEYUP:

            if raw.key == pygame.K_LEFT:

                down['left'] = False

            elif raw.key == pygame.K_RIGHT:

                down['right'] = False

        self.__raw = raw

        logger.info("Wrapping Event created")
        logger.info("Window closed: %s", self.quit())
        logger.info("Escape pressed: %s", self.escape())
        logger.info("Left is %s", "down" if self.left_is_down() else "up")
        logger.info("Right is %s", "down" if self.right_is_down() else "up")
        logger.info("Jump pressed: %s", self.jump_pressed())

    def quit(self):

        raw = self.__raw

        return raw.type == pygame.QUIT

    def escape(self):

        raw = self.__raw

        return (raw.type == pygame.KEYDOWN and
                raw.key == pygame.K_ESCAPE)

    def left_is_down(self):

        return down['left']

    def right_is_down(self):

        return down['right']

    def jump_pressed(self):

        raw = self.__raw

        return (raw.type == pygame.KEYDOWN and
                raw.key == pygame.K_SPACE)


class QEngine(SDL):

    def input(self):

        raw_evt = super(QEngine, self).input()

        return Event(raw_evt)
