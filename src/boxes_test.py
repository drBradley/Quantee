# -*- coding: utf-8 -*-


import random
import unittest

from boxes import Box, Boxes


CASE_COUNT = 10000

MAX_X = MAX_Y = MAX_W = MAX_H = 100


def complement(box):

    if isinstance(box, Box):
        b0 = Box(0, 0, box.x, MAX_Y + MAX_H)
        b1 = Box(box.x, box.y + box.h, box.w, MAX_Y + MAX_H - box.y - box.h)
        b2 = Box(box.x, 0, box.w, box.y)
        b3 = Box(box.x + box.w, 0, MAX_X + MAX_W - box.x - box.w)

        return b0 | b1 | b2 | b3

    elif isinstance(box, Boxes):

        everything = Box(0, 0, MAX_X + MAX_W, MAX_Y + MAX_H)

        return reduce(lambda a, b: a & b, map(complement, box), everything)


class OperationTest(unittest.TestCase):
    """Common base class for operation tests -- sets up the test cases"""

    def setUp(self):
        self.cases = []
        for i in range(CASE_COUNT):
            a = Box(
                    random.randint(0, MAX_X),
                    random.randint(0, MAX_Y),
                    random.randint(0, MAX_W),
                    random.randint(0, MAX_H))

            b = Box(
                    random.randint(0, MAX_X),
                    random.randint(0, MAX_Y),
                    random.randint(0, MAX_W),
                    random.randint(0, MAX_H))

            c = Box(
                    random.randint(0, MAX_X),
                    random.randint(0, MAX_Y),
                    random.randint(0, MAX_W),
                    random.randint(0, MAX_H))

            self.cases.append((a, b, c))

        self.points = []

        for i in range(CASE_COUNT):
            self.points.append((
                    random.randint(0, MAX_X + MAX_W),
                    random.randint(0, MAX_Y + MAX_H)))


class UnionTest(OperationTest):
    """Test whether set unions work properly"""

    def test_associative(self):

        for a, b, c in self.cases:

            d = (a | b) | c
            e = a | (b | c)

            for point in self.points:

                self.assertEqual(point in d, point in e)

    def test_commutative(self):

        for a, b, _ in self.cases:

            d = a | b
            e = b | a

            for point in self.points:

                self.assertEqual(point in d, point in e)

    def test_complement(self):

        for case in self.cases:
            for a in case:
                d = a | complement(a)

                for point in self.points:

                    self.assertIn(point, d)

    def test_with_self(self):

        for case in self.cases:
            for a in case:

                d = a | a

                for point in self.points:

                    self.assertEqual(
                            point in d,
                            point in a)

    def test_with_subset(self):

        for case in self.cases:
            for a in case:

                if not (a.w >= 2 and a.h >= 2):
                    continue

                b = Box(a.x + 1, a.y + 1, a.w - 1, a.h - 1)

                d = a | b

                for point in self.points:

                    self.assertEqual(
                            point in d,
                            point in a)


class IntersectionTest(OperationTest):
    """Test whether set intersections work properly"""

    def test_associative(self):

        for a, b, c in self.cases:

            d = (a & b) & c
            e = a & (b & c)

            for point in self.points:

                self.assertEqual(point in d, point in e)

    def test_commutative(self):

        for a, b, _ in self.cases:

            d = a & b
            e = b & a

            for point in self.points:

                self.assertEqual(point in d, point in e)

    def test_complement(self):

        for case in self.cases:
            for a in case:
                d = a & complement(a)

                for point in self.points:

                    self.assertNotIn(point, d)

    def test_with_self(self):

        for case in self.cases:
            for a in case:

                d = a & a

                for point in self.points:

                    self.assertEqual(
                            point in d,
                            point in a)

    def test_with_subset(self):
        pass

    def test_with_disjoint(self):

        for case in self.cases:
            for a in case:

                if not (a.w >= 2 and a.h >= 2):
                    continue

                b = Box(a.x + 1, a.y + 1, a.w - 1, a.h - 1)

                d = a & b

                for point in self.points:

                    self.assertEqual(
                            point in d,
                            point in b)


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
        (x | y) & z = (x & z) | (y & z)
        x & (y | z) = (x & y) | (x & z)
        (x & y) | z = (x | z) & (y | z)
    """

    def union_left_distributive(self):
        pass

    def intersection_left_distributive(self):
        pass

    def intersection_right_distributive(self):
        pass

    def union_right_distributive(self):
        pass
