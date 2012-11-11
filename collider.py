# -*- coding: utf-8 -*-


__all__ = ['Collider']


class Collider(object):
    """Abstract base class for Colliders"""

    def __and__(self, other):
        """C & other -> another Collider or None"""

        raise NotImplementedError()
