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


import logging

from boxes import collide

__all__ = ['DrawingStrategy', 'Everyone', 'DirtyWholes']


logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


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

    def __init__(self):

        logger.warning('DrawingStrategies are soon to be deprecated!')

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

        logger.warning('DrawingStrategies are soon to be deprecated!')

        self.__active_stage_id = id(None)

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

        on_screen = collide(
            entity.present().r_box(),
            viewport)

        was_on_screen = collide(
            entity.past().r_box(),
            viewport)

        # Thing that are and were on screen have quite a couple of rules...
        if on_screen and was_on_screen:

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

        # Entities that change their onscreen status are dirty
        elif on_screen != was_on_screen:

            return True

        return False

    def render(self, stage, engine, viewport):

        if id(stage) != self.__active_stage_id:

            stage.add_death_observer(self)
            self.__active_stage_id = id(stage)

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

        # Clear up
        self.__dirty.clear()
        self.__force_all = False
