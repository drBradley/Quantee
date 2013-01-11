# -*- coding: utf-8 -*-


from boxes import collide


__all__ = ['DrawingStrategy', 'Everyone', 'DirtyWholes']


class DrawingStrategy(object):
    """Base class for objects deciding what exactly to draw during a rendering
    pass.
    """

    def force_all(self):
        """DS.force_all()

        Forces all visible entities to be drawn once, neglecting the normal
        behaviour of the strategy.
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

    def force_all(self):

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
        self.__drawn = set()

        self.__force_all = False

    def tell_is_dead(self, entity):

        self.__dirty.add(entity)
        self.__mark_drawn(entity, False)

    def force_all(self):

        self.__force_all = True

    def __was_drawn(self, entity):

        return entity in self.__drawn

    def __mark_drawn(self, entity, dont_flip=True):

        if dont_flip and entity in self.__drawn:

            self.__drawn.remove(entity)

        else:

            self.__drawn.add(entity)

    def __is_dirty(self, entity, viewport, others=set()):

        # Something that isn't on screen never needs to be redrawn
        if collide(entity.present().r_box(), viewport):

            # Is the stretegy being suppresed?
            if self.__force_all:

                return True

            # Force the drawing of new Entities first time they apppear on
            # screen
            if not self.__was_drawn(entity):

                self.__mark_drawn(entity)

                return True

            # See if a redraw is necessary due to changes in the entity itentity
            moved = entity.present().r_box() != entity.past().r_box()

            sprite_changed = \
                entity.present().state_name() != entity.past().state_name()

            if moved or sprite_changed:
                return True

            # See if a redraw is necessary due to changes around the entity
            for other in others:

                collided = collide(
                    entity.past().r_box(),
                    other.past().r_box())

                collide_now = collide(
                    entity.present().r_box(),
                    other.present().r_box())

                if collided or collide_now:
                    return True

        return False

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

        # Clear up
        self.__dirty.clear()
        self.__force_all = False
