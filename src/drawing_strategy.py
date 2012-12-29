# -*- coding: utf-8 -*-


from boxes import collide


__all__ = ['DrawingStrategy', 'Everyone', 'DirtyWholes']


class DrawingStrategy(object):
    """Base class for objects deciding what exactly to draw during a rendering
    pass.
    """

    def tell_is_dead(self, entity):
        """DS.tell_is_dead(entity)

        Notify the DrawingStrategy that an Entity has died.
        """

        raise NotImplementedError()

    def render(self, stage, engine, viewport):
        """DS.render(stage, engine, viewport)

        Renders the visible part of the stage using the viewport.
        """

        raise NotImplementedError()


class Everyone(DrawingStrategy):
    """A drawing strategy that draws everything that collides with the
    viewport.
    """

    def tell_is_dead(self, entity):

        pass

    def render(self, stage, engine, viewport):

        for entity in stage:

            if collide(entity.present().r_box(), viewport):

                entity.draw(engine, viewport)


class DirtyWholes(DrawingStrategy):
    """Drawing strategy that doesn't redraw Entities which don't have to be
    redrawn."""

    def __init__(self):

        self.__dirty = set()

    def tell_is_dead(self, entity):

        self.__dirty.add(entity)

    def __is_dirty(self, entity, viewport, others=set()):

        return entity.needs_redraw(viewport, others)

    def render(self, stage, engine, viewport):

        dirty, maybe = self.__dirty, set()

        for entity in stage:

            if self.__is_dirty(entity, viewport):

                dirty.add(entity)

            else:

                maybe.add(entity)

        # Find all those who need redraw amongst those who might
        any_new = True

        while any_new:

            any_new = False

            for entity in maybe:

                if self.__is_dirty(entity, viewport, dirty):

                    dirty.add(entity)

                    any_new = True

            maybe.difference_update(dirty)

        # Redraw only those who need it
        for entity in stage:

            if entity in dirty:

                entity.draw(engine, viewport)

        print "Redrawn %d entities" % len(dirty)

        # Same as self.__dirty.clear()
        dirty.clear()
