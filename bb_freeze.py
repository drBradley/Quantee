#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from bbfreeze import Freezer


f = Freezer('quantee',
            includes=['pygame'],
            excludes=['numpy'])

f.addScript('src/quantee.py')
f()
