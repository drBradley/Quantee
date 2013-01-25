# -*- coding: utf-8 -*-

import pygame

from sdl import SDL


__all__ = ['QEngine']


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
