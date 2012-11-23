# -*- coding: utf-8 -*-


__all__ = ['Box']


class Box(object):
    """Box(x, y, w, h) -> a Box

    The simplest possible Collider.
    """

    def __init__(self, x, y, w, h):

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __contains__(self, point):

        x_p, y_p = point

        return (self.x <= x_p <= self.x + self.w and
                self.y <= y_p <= self.y + self.h)

    def __str__(self):

        return "Box(%(x)d, %(y)d, %(w)d, %(h)d)" % self.__dict__

    def move_by(self, dx, dy):
        """B.move_by(dx, dy)

        Moves the box by a given distance.
        """

        self.x += dx
        self.y += dy
