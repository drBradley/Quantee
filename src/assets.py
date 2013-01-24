# -*- coding: utf-8 -*-


import os

import pygame

from sdl import AssetManager

__all__ = ['QAssets']


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

        return self.__sprites[name]

    def clear_cache(self):

        self.__sprites = {}
