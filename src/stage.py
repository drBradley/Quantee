# -*- coding: utf-8 -*-


__all__ = ['Stage']


class Stage(object):
    """Stage((width, height), layers, default_layer) -> a new Stage

    Stages store Entities in layers.

    Layers are all named. Layers and the Entities in them have a set order.
    """

    def __init__(self, size, layers, default_layer):

        # Camera-related fields
        self.__size = size
        self.__cam_at = None

        # Entity storage-related fields
        self.__layers = {}
        self.__spawns = {}

        self.__layer_names = layers
        self.__default_layer = default_layer

        for layer in layers:

            self.__layers[layer] = []
            self.__spawns[layer] = []

    def __iter__(self):
        """S.__iter__() <=> iter(S)"""

        for name in self.__layer_names:

            layer = self.__layers[name]

            for entity in layer:

                yield entity

    @property
    def size(self):
        """S.size -> (width, height)"""

        return self.__size

    # Logic
    def harvest_dead(self):
        """S.harvest_dead()

        Remove all the dead Entities from the Stage.
        """

        dead = {}

        # Find the indices of dead Entities in each layer
        for name in self.__layers:

            dead[name] = []

            for i, entity in enumerate(self.__layers[name]):

                if entity.present().dead():

                    dead[name].insert(0, i)

        # Remove the dead Entities from each layer
        #
        # First removes the ones with bigger indices, so the indices of the
        # rest need not be adjusted
        for name in dead:

            for i in dead[name]:

                self.__layers[name].pop(i)

    def add_spawn(self, entity, layer=None):
        """S.add_spawn(entity[, layer])

        Add an Entity to be spawned in the next iteration.
        """

        if layer is None:
            layer = self.__default_layer

        if layer not in self.__layer_names:
            raise ValueError('Non-existent layer name')

        self.__spawns[layer].append(entity)

    def spawn(self):
        """S.spawn()

        Spawns all the Entities scheudled for spawning.
        """

        for name in self.__layer_names:

            self.__layers[name].extend(self.__spawns[name])

            self.__spawns[name] = []

    # Rendering
    def render(self, engine, viewport):
        """S.render(engine, viewport)

        Render the part of the stage described by viewport using the engine.
        """

        # Separate the entities clearly needing a redraw and the ones that
        # might need it
        redraw, maybe = set(), set()

        for entity in self:

            if entity.needs_redraw(viewport):

                redraw.add(entity)

            else:

                maybe.add(entity)

        # Find all those who need redraw amongst those who might
        any_new = True

        while any_new:

            any_new = False

            for entity in maybe:

                if entity.needs_redraw(viewport, redraw):

                    redraw.add(entity)

                    any_new = True

            maybe.difference_update(redraw)

        # Redraw only those who need it
        for entity in self:

            if entity in redraw:

                entity.draw(engine, viewport)
