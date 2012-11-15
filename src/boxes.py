# -*- coding: utf-8 -*-


from collider import Collider

__all__ = ['Box', 'Boxes']


def intersect_edges(box1, box2):

    edges1 = set()
    edges2 = set()

    # Edges are tupples of one bool and three ints
    #
    # The bool tell us whether the edge is vertical
    # The first int is the redundant coordinate
    # The other two are the differing ones (in ascending order)
    for edges, box in ((edges1, box1), (edges2, box2)):
        edges.add((False, box.y, box.x, box.x + box.w))
        edges.add((False, box.y + box.h, box.x, box.x + box.w))
        edges.add((True, box.x, box.y, box.y + box.h))
        edges.add((True, box.x + box.w, box.y, box.y + box.h))

    for edge1 in edges1:
        vert1, const1, fst1, snd1 = edge1

        for edge2 in edges2:
            vert2, const2, fst2, snd2 = edge2

            if (vert1 != vert2 and
                    fst2 <= const1 <= snd1 and
                    fst1 <= const2 <= snd2):
                yield (const1, const2) if vert2 else (const2, const1)


class Box(Collider):
    """Box(x, y, w, h) -> a Box

    The simplest possible Collider.
    """

    def __init__(self, x, y, w, h):

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __contains__(self, point):

        x_p, y_p = point

        return (self.x <= x_p <= self.x + self.w and
                self.y <= y_p <= self.y + self.h)

    def __and__(self, other):

        if not isinstance(other, Box):
            return NotImplemented

        points = set()

        for b in (self, other):

            points.add((b.x, b.y))
            points.add((b.x + b.w, b.y))
            points.add((b.x, b.y + b.h))
            points.add((b.x + b.w, b.y + b.h))

        for p in intersect_edges(self, other):

            points.add(p)

        corners = []

        for point in points:
            if point in self and point in other:
                corners.append(point)

        corners.sort()

        x, y = corners[0]
        x_w, y_h = corners[-1]

        w, h = x_w - x, y_h - y

        return Box(x, y, w, h)

    def move_by(self, dx, dy):
        """B.move_by(dx, dy)

        Moves the box by a given distance.
        """

        self.x += dx
        self.y += dy


class Boxes(Collider, list):
    """Boxes() -> empty Box container
    Boxes(iterable) -> a Box container initialised from iterable's items

    A list-based container for Boxes. Supports all operations supported by
    lists and Colliders.
    """

    def __init__(self, iterable=[]):
        super(list, self).__init__(iterable)

    def __and__(self, other):

        if not isinstance(other, (Box, Boxes)):
            return NotImplemented

        result = Boxes()

        if isinstance(other, Box):
            many = False
        else:
            many = True

        for box in self:
            common = box & other

            if common is not None:
                if many:
                    result.extend(common)
                else:
                    result.append(common)

        return result

    def move_by(self, dx, dy):
        """B.move_by(dx, dy)

        Move the Boxes by a given distance.
        """

        for box in self:
            box.move_by(dx, dy)
