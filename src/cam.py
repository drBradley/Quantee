# -*- coding: utf-8 -*-


__all__ = ['Cam', 'StaticCam']


class Cam(object):
    """Abstract base class for Cams"""

    def viewport(self, stage):
        """C.viewport() -> a Box

        The part of a Level to be mapped on-screen.

        The behaviour of an Engine when the Box's ratio is different from the
        one of the screen is undefined.
        """


class StaticCam(Cam):
    """StaticCam(box) -> a Cam always returning the same viewport"""

    def __init__(self, box):

        self.__box = box

    def viewport(self, stage):
        """SC.viewport() -> always the same Box"""

        return self.__box
