# -*- coding: utf-8 -*-


__all__ = ['Director']


class Director(object):
    """Abstract base class for Directors.

    Provides
    """

    def hints(self, entity):
        """D.hints(entity) -> extra data an entity might want to get from the
        Director
        """

        raise NotImplementedError()

    def orchestrate(self, dt, event, stage, levels):
        """D.orchestrate(dt, event, stage, levels)

        Manage the scene and game flow.
        """

        raise NotImplementedError()

    def viewport(self, stage):
        """D.viewport(stage) -> a Box describing the visible part of the screen
        """

        raise NotImplementedError()
