#-*- coding: utf-8 -*-
'''
@author: Christian Caspers
'''
import re
import numpy as np
from OpenGL.arrays import vbo
from math import cos, sin, sqrt

class Model(object):
    '''
    Model that contains triangles and provides them as VBO
    Encapsulates logic for rotation, scaling and translation
    '''
    
    NORM_SIZE = 2.

    def __init__(self, faces):
        self.faces = faces
        self.scale = 1
        self.faces_vbo_cache = None
        self.position = (0.0, 0.0, 0.0)
        self.orientation = np.matrix([[1.0, 0.0, 0.0, 0.0],
                                      [0.0, 1.0, 0.0, 0.0],
                                      [0.0, 0.0, 1.0, 0.0],
                                      [0.0, 0.0, 0.0, 1.0]])
        self.rotate()
        
    def rotate(self, angle=0, axis=(0, 1.0, 0)):
        axis = np.array(axis)
        c, mc = cos(angle), 1-cos(angle)
        s = sin(angle)
        l = sqrt(np.dot(axis,axis))
        if l != 0:
            x, y, z = axis / l
            r = np.matrix([[x*x*mc + c  ,  x*y*mc - z*s,  x*z*mc + y*s,  0],
                           [y*x*mc + z*s,  y*y*mc + c  ,  y*z*mc - x*s,  0],
                           [z*x*mc - y*s,  z*y*mc + x*s,  z*z*mc + c  ,  0],
                           [0           ,  0           ,  0           ,  1]])
            self.rotation = r.transpose()
            
    def getRotationMatrix(self):
        return self.orientation * self.rotation
    
    def saveOrientation(self):
        self.orientation *= self.rotation
        self.rotate()
        
    def adjustScale(self, deltaScale):
        newScale = self.scale + deltaScale * Model.NORM_SIZE
        self.scale = newScale if newScale > 0 else self.scale
    
    def move(self, deltaX, deltaY):
        deltaX = deltaX * Model.NORM_SIZE / self.scale
        deltaY = deltaY * Model.NORM_SIZE / self.scale
        x,y,z = self.position
        self.position = (x + deltaX, y + deltaY, z)
        
    @property
    def faces_vbo(self):
        if not self.faces_vbo_cache:
            self.faces_vbo_cache = vbo.VBO(np.array(self.faces, 'f'))
        return self.faces_vbo_cache 
        
    def getBoundingBox(self):
        return [[func([t[i] for t in self.faces])for i in range(3)] for func in (min, max)]
    
    def normalized(self):
        return self._normalizedScale()._movedToZero()
    
    def _movedToZero(self):
        center = self._getCenter()
        return Model([[x - y for x, y in zip(t, center)] for t in self.faces])
    
    def _normalizedScale(self):
        scalefactor = Model.NORM_SIZE / max([abs(maxV - minV) for minV, maxV in zip(*self.getBoundingBox())])
        return Model([t * scalefactor for t in self.faces])    
    
    def _getCenter(self):
        return [(x + y) / 2 for x, y in zip(*self.getBoundingBox())]
    
    
def calculateDistance(pointA, pointB):
    vector = [x - y for x, y in zip(pointA, pointB)]
    return sqrt(sum([t ** 2 for t in vector]))


def parse(objFile):
    contents = file(objFile).readlines()
    
    v = parseVertices(contents)
    v_indexes = parseFaces(contents)
    faces = [v[x] for x in v_indexes]
    return Model(faces).normalized()


def parseVertices(contents):
    return parseCoordinates(contents, "v")


def parseFaces(contents):
    prefix = "f"
    lines =  extractMatch(contents, prefix + " .")
    lines = [line.strip(prefix + " ").split() for line in lines]
    faces = [extract_vIndexes(line) for line in lines]
    return [item for sublist in faces for item in sublist]


def extract_vIndexes(line):
    return [[int(t) - 1 if t else None for t in coord.split("/")][0] for coord in line]
        
        
def parseCoordinates(contents, prefix):
    lines =  extractMatch(contents, prefix + " .")
    return [makeCoordinatesFrom(line, prefix) for line in lines]


def extractMatch(values, pattern):
    return [t for t in values if re.match(pattern, t)]


def makeCoordinatesFrom(line, replace):
    return np.array([float(x) for x in line.strip(replace+" ").split()])


