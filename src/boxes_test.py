# -*- coding: utf-8 -*-


import random
import unittest

from boxes import Box, Boxes


class UnionTest(unittest.TestCase):
    """Test whether set unions work properly"""

    def test_associative(self):
        pass

    def test_commutative(self):
        pass

    def test_complement(self):
        pass

    def test_with_self(self):
        pass

    def test_with_subset(self):
        pass


class IntersectionTest(unittest.TestCase):
    """Test whether set intersections work properly"""

    def test_associative(self):
        pass

    def test_complement(self):
        pass

    def test_with_self(self):
        pass

    def test_with_subset(self):
        pass

    def test_with_disjoint(self):
        pass


class DeMorganTest(unittest.TestCase):
    """Test whether the union and set operations obey the DeMorgan's Laws:

        not (p & q) = (not p) | (not q)
        not (p | q) = (not p) & (not q)

    (Note that `not` is not defined for out sets.)
    """

    def first_law(self):
        pass

    def second_law(self):
        pass


class DistributiveTest(unittest.TestCase):
    """Test whether the set operations are distributive, ie:

        x | (y & z) = (x | y) & (x | z)
        x & (y | z) = (x & y) | (x & z)
    """

    def union_left_distributive(self):
        pass

    def intersection_left_distributive(self):
        pass

    def intersection_right_distributive(self):
        pass

    def union_right_distributive(self):
        pass
