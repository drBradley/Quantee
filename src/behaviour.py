# -*- coding: utf-8 -*-


class Behaviour(object):

    def prepare(self, curr, next):

        raise NotImplementedError()

    def decide(self, dt, event, stage, curr, next):

        raise NotImplementedError()
