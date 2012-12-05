# -*- coding: utf-8 -*-


import os

from sdl import AssetManager

__all__ = ['QAssets']


class QAssets(AssetManager):

    def __init__(self, asset_dir=None):

        if not isinstance(asset_dir, basestring):
            asset_dir = os.getenv('QUANTEE_ASSETS', './assets')

        self.__asset_dir = os.path.abspath(asset_dir)

        self.__sprites = {}

    def load_spirte(self, name, no_cache=False):

        if name not in self.__sprites or no_cache:

            # TODO: Load the sprite
            pass

        return self.__sprites[name]

    def clear_cache(self):

        self.__sprites = {}
