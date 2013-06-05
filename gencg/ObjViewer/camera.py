#-*- coding: utf-8 -*-
'''
@author: Christian Caspers
'''
class Camera(object):
    '''
    Camera-Object that contains intrinsic and extrinsic parameters.
    As of now, only zoom-functions are provided
    '''
    
    def __init__(self, eye = (0., 0., 4.), center = (0. ,0. ,0), up=(0., 1., 0.)):
        self.eye = eye
        self.center = center
        self.up = up
        self.fov = 30.
        self.zoom = 1.0
        
    def adjust_zoom(self, deltaZoom):
        self.zoom += deltaZoom
        
    def __str__(self):
        return "Camera eye=%s, center=%s, up=%s" % (self.eye, self.center, self.up)