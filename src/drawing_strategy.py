# -*- coding: utf-8 -*-


from boxes import collide


__all__ = ['DrawingStrategy', 'Everyone']


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
