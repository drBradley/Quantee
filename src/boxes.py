# -*- coding: utf-8 -*-


__all__ = ['Box']


def bounding(b1, b2):

    xcoors = [b1.x, b1.x + b1.w, b2.x, b2.x + b2.w]
    ycoors = [b1.y, b1.y + b1.h, b2.y, b2.y + b2.h]

    xcoors.sort()
    ycoors.sort()

    x = xcoors[0]
    y = ycoors[0]
    w = xcoors[-1] - xcoors[0]
    h = ycoors[-1] - ycoors[0]

    return Box(x, y, w, h)


def collide(b1, b2):

    if ((b2.x + b2.w <= b1.x or
         b1.x + b1.w <= b2.x) and

        (b2.y >= b1.x + b1.h or
         b2.y + b2.h <= b1.y)):

        return False

    return True


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
