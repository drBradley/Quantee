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

import os
import logging

import pygame

from sdl import AssetManager

__all__ = ['QAssets']


logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


class QAssets(AssetManager):

    def __init__(self, color_key, asset_dir=None):

        if not isinstance(asset_dir, basestring):
            asset_dir = os.getenv('QUANTEE_ASSETS', './assets')

        self.__color_key = color_key

        self.__asset_dir = os.path.abspath(asset_dir)

        self.__sprites = {}

    def load_sprite(self, name, no_cache=False):

        if name not in self.__sprites or no_cache:

            path = os.path.join(self.__asset_dir,
                                'sprites',
                                name + '.png')

            sprite = pygame.image.load(path)
            sprite.set_colorkey(self.__color_key)
            sprite = sprite.convert()

            self.__sprites[name] = sprite

            logger.info("Sprite %s loaded into cache", name)

        logger.info("Sprite %s retrieved from cache", name)
        return self.__sprites[name]

    def clear_cache(self):

        logger.info("Sprite cache cleared")
        self.__sprites = {}
