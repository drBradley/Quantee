# -*- coding: utf-8 -*-


import logging


__all__ = ['Stage']


logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


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

        # To properly render everything we need to keep track of what dies
        self.__dirty = set()
        self.__death_observers = []

        logger.info('%dx%d Stage created', size[0], size[1])
        logger.info('%d layers created: %s', len(layers), layers)

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

                corpse = self.__layers[name].pop(i)

                self.__dirty.add(corpse)

                # Notify everyone who might be interested
                for death_observer in self.__death_observers:

                    death_observer.tell_is_dead(corpse)

        logger.info('Dead harvested')

    def add_spawn(self, entity, layer=None):
        """S.add_spawn(entity[, layer])

        Add an Entity to be spawned in the next iteration.
        """

        if layer is None:
            layer = self.__default_layer

        if layer not in self.__layer_names:
            raise ValueError('Non-existent layer name')

        self.__spawns[layer].append(entity)

        logging.debug(
            '%s will be spawned in %s the next physics step',
            entity,
            layer)

    def spawn(self):
        """S.spawn()

        Spawns all the Entities scheudled for spawning.
        """

        for name in self.__layer_names:

            for spawn in self.__spawns[name]:

                logger.debug('Spawning %s in %s',
                             spawn,
                             name)

            self.__layers[name].extend(self.__spawns[name])

            self.__spawns[name] = []

    def add_death_observer(self, observer):
        """S.add_death_observer(observer)

        Adds a new observer of dying entities."""

        self.__death_observers.append(observer)

        logger.info('%s now observes the deaths in %s',
                    observer,
                    self)
