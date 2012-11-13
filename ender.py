# -*- coding: utf-8 -*-


__all__ = ['Ender']


class Ender(object):
    """Abstract base class for Enders.

    Enders are objects which determine whether a Level should end and what
    Level (if any) should the Game run afterwards.
    """

    def done(self, dt, event, stage):
        """E.done(dt, event, stage) -> True or False

        Decides whether an Level should end.
        """

    def next_level(self):
        """E.next_level() -> another Level or None"""
