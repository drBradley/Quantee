# -*- coding: utf-8 -*-


from collider import Collider

__all__ = ['Box', 'Boxes']


class Box(Collider):
    """Box(x, y, w, h) -> a Box

    The simplest possible Collider.
    """

    def __init__(self, x, y, w, h):

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __and__(self, other):

        if not isinstance(other, Box):
            return NotImplemented

        raise NotImplementedError()


class Boxes(Collider, list):
    """Boxes() -> empty Box container
    Boxes(iterable) -> a Box container initialised from iterable's items

    A list-based container for Boxes. Supports all operations supported by
    lists and Colliders.
    """

    def __init__(self, iterable=[]):
        super(list, self).__init__(iterable)

    def __and__(self, other):

        if not isinstance(other, (Box, Boxes)):
            return NotImplemented

        result = Boxes()

        if isinstance(other, Box):
            many = False
        else:
            many = True

        for box in self:
            common = box & other

            if common is not None:
                if many:
                    result.extend(common)
                else:
                    result.append(common)

        return result
