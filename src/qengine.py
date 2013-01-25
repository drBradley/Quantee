# -*- coding: utf-8 -*-

import pygame

from sdl import SDL


__all__ = ['QEngine']


class Event(object):
    """Wrapper for raw SDL events used in QTG"""

    def __init__(self, raw_evt):

        self.__raw_evt = raw_evt

    def quit(self):

        raw = self.__raw_evt

        return raw.type is pygame.QUIT

    def escape(self):

        raw = self.__raw_evt

        return (raw.type is pygame.KEYDOWN and
                raw.key is pygame.K_ESCAPE)


class QEngine(SDL):

    def input(self):

        raw_evt = super(QEngine, self).input()

        return Event(raw_evt)
