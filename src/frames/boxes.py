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


def __corners(box, margin):

    if isinstance(margin, tuple) and len(margin) == 2:

        mx, my = margin

    else:

        mx = margin
        my = margin

    for x in (box.x - mx, box.x + box.w + mx):

        for y in (box.y - my, box.y + box.h + my):

            yield (x, y)


def collide(a, b, margin=0):

    for a_point in __corners(a, margin):

        if a_point in b:

            return True

    for b_point in __corners(b, margin):

        if b_point in a:

            return True

    return False


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

    def __eq__(self, other):

        return (self.x == other.x and
                self.y == other.y and
                self.w == other.w and
                self.h == other.h)

    def __ne__(self, other):

        return not self == other

    def __str__(self):

        return "Box(%(x)d, %(y)d, %(w)d, %(h)d)" % self.__dict__

    def move_by(self, dx, dy):
        """B.move_by(dx, dy)

        Moves the box by a given distance.
        """

        self.x += dx
        self.y += dy

    def move_to(self, x, y):
        """B.move_to(x, y)

        Moves the box to a given position.
        """

        self.x = x
        self.y = y
