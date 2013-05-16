import math
import numpy as np
from model import Model


class Camera(object):

    def __init__(self, up, focus, width, height, Far=4, Near=1.1):
        ''' initializing camera with default values '''
        self.u = self.up = np.array(up)
        self.f = self.focus = np.array(focus)
        self.aspect = float(width) / float(height)
        self.Far = float(Far)
        self.Near = float(Near)
        self.position = np.array((0, 0, 0))
        # init matrix to default
        self.MLookAt = np.matrix(((1, 0, 0, 0),
                                  (0, 1, 0, 0),
                                  (0, 0, 1, 0),
                                  (0, 0, 0, 1)), np.float)
        self.fullMatrix = self.MLookAt

    def renderModel(self, model):
        points = [np.array(tuple(point)) for point in model.points]
        points = [np.resize(v, (1,4)) * self.fullMatrix for v in points]
        points = [point.getA1() for point in points]
        points = [(x / w, y / w, z / w) for x, y, z, w in points]
        # Transform Perspective
        return Model(points)

    def _calculatePerspectiveMatrix(self):
        angle = math.radians(30)
        cotan = math.cos(angle) / math.sin(angle)
        a = cotan / self.aspect
        b = cotan
        c = -(self.Far + self.Near) / (self.Far - self.Near)
        d = -(2 * self.Far * self.Near) / (self.Far - self.Near)
        matrix = np.matrix(((a,  0,  0,  0),
                            (0,  b,  0,  0),
                            (0,  0,  c,  d),
                            (0,  0, -1,  0)), np.float)
        return matrix

    def setupCameraForModel(self, model):
        # Update CoordinateSystem for View at Model
        self._updateCoordinateSystem(model)
        # Create Matrix for Transformation
        self.MLookAt = self._updateLookAtMatrix()
        self.fullMatrix = self._calculatePerspectiveMatrix() * self.MLookAt

    def _updateLookAtMatrix(self):
        s, u, f, e = self.s, self.u, self.f, self.position
        MLookAt = np.matrix(((s[0], u[0], -f[0], e[0]),
                                  (s[1], u[1], -f[1], e[1]),
                                  (s[2], u[2], -f[2], e[2]),
                                  (   0,    0,     0,    1)), np.float) #@IgnorePep8
        return MLookAt

    def _calculatePosition(self, model):
        distance = 2 * model.getMinimalRadius()
        return np.array((0, 0, -distance), np.float)

    def _updateCoordinateSystem(self,model):
        self.position = self._calculatePosition(model)
        uu = _norm(self.up)
        self.f = _norm((self.position - self.focus))
        self.s = _norm(np.cross(self.f, uu))
        self.u = np.cross(self.s, self.f)
        


def _norm(v):
    return v / np.linalg.norm(v)
