import math
import numpy as np
import itertools


class Model(object):

    def __init__(self, points=[]):
        self.points = points

    def getBoundingBox(self):
        return [[func([t[i] for t in self.points])for i in range(3)] for func in (min, max)]

    def _movedToZero(self):
        center = self._getCenter()
        return Model([[x - y for x, y in zip(t, center)] for t in self.points])

    def _normalizedScale(self):
        scalefactor = 2 / max([abs(maxV - minV) for minV, maxV in zip(*self.getBoundingBox())])
        return Model([[x * scalefactor for x in t] for t in self.points])

    def normalized(self):
        return self._normalizedScale()._movedToZero()

    def rotated(self, angleInDegree):
        return Model([_rotatePoint(p, angleInDegree) for p in self.points])

    def _getCenter(self):
        return [(x + y) / 2 for x, y in zip(*self.getBoundingBox())]

    def getMinimalRadius(self):
        edges = self._calculateCornerPoints()
        center = self._getCenter()
        return min([calculateDistance(center, point) for point in edges])

    def _calculateCornerPoints(self):
        points = self.getBoundingBox()
        selection = [seq for seq in itertools.product((0, 1), repeat=3)]
        return [(points[x][0], points[y][1], points[z][2])
                for x, y, z in selection]


def calculateDistance(pointA, pointB):
    vector = [x - y for x, y in zip(pointA, pointB)]
    return math.sqrt(sum([t ** 2 for t in vector]))


def _rotatePoint(p, angleInDegree):
    x, y, z = p
    angle = math.radians(angleInDegree)
    sinAngle = math.sin(angle)
    cosAngle = math.cos(angle)
    return (x * cosAngle + z * sinAngle,
            y,
            z * cosAngle - sinAngle * x)


def parse(filename):
    return Model([np.array(t.split(), np.float) for t in file(filename).readlines()])

