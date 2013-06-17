#-*- coding: utf-8 -*-
'''
@author: Christian Caspers
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from model import Model
import q
import glhelper as glh

X_AXIS = (1.0, 0.0, 0.0)
Y_AXIS = (0.0, 1.0, 0.0)
Z_AXIS = (0.0, 0.0, 1.0)

BLACK  = (0.0, 0.0, 0.0, 0.0)
WHITE  = (1.0, 1.0, 1.0, 0.0)
RED    = (1.0, 0.0, 0.0, 0.0)
GREEN  = (0.0, 1.0, 0.0, 0.0)
BLUE   = (0.0, 0.0, 1.0, 0.0)
YELLOW = (1.0, 1.0, 0.0, 0.0)

COLORS = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW]

class Renderer(object):
    '''
    Encapsulates the rendering logic and provides
    functions to switch colors, projection-types
    and adapt to screen-configuration-changes
    '''
    @q
    def __init__(self, model, camera, width, height):
        self.model = model
        self.camera = camera
        self.foreground_color = COLORS.index(WHITE)
        self.background_color = COLORS.index(BLUE)
        self.orthogonal = True
        # Initialize the window
        glClearColor(*BLACK)
        glColor4f(*COLORS[self.foreground_color])
        self.reshape(width, width)
        
    @q
    def display(self):
        """ Render all objects"""
        glh.matrixMode(GL_MODELVIEW)
        self.resetCurrentBuffer()
        self.renderModel()
        glutSwapBuffers()
    
    @q    
    def resetCurrentBuffer(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    @q    
    def updateCamera(self):
        glh.matrixMode(GL_MODELVIEW)
        glh.loadIdentity()
        ex, ey, ez = self.camera.eye
        cx, cy, cz = self.camera.center
        ux, uy, uz = self.camera.up
        glh.lookAt(ex, ey, ez,
                  cx, cy, cz,
                  ux, uy, uz)
    
    @q    
    def renderModel(self):
        glh.matrixMode(GL_MODELVIEW)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glh.pushMatrix()
        
        vbo = self.model.faces_vbo
        
        scale = self.model.scale
        glh.multMatrix(self.model.getRotationMatrix())
        glh.scale(scale, scale, scale)
        glh.translate(*self.model.position)
                       
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        vbo.bind()
        glVertexPointerf(vbo)
        glNormalPointerf(vbo + (len(self.model.faces)* 3 * 4))

        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces))
        
        lightPos = [0, 0, -11]
        diffCol = [0.7059, 0.3922, 0.2353, 1]
        ambCol = [0.1765, 0.0980, 0.0588, 1]
        specCol = [0.3529, 0.1961, 0.1176, 1]
        
        glh.sendVec4("diffuseColor", diffCol)
        glh.sendVec4("ambientColor", ambCol)
        glh.sendVec4("specularColor", specCol)
        glh.sendVec3("lightPosition", lightPos)
        
        vbo.unbind()
        
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glh.popMatrix()
    
    @q
    def reshape(self, width, height):
        """ adjust projection matrix to window size"""
        glViewport(0,0,width, height)
        glh.matrixMode(GL_PROJECTION)
        glh.loadIdentity()
        self.setupPerspectiveProjection(width, height)
        self.updateCamera()
    
    @q              
    def setupPerspectiveProjection(self, width, height):
        aspect = float(width)/float(height)
        glh.perspective(self.camera.fov, aspect, 1.0, 100.0)
    
    @q        
    def cycleForegroundColor(self):
        self.foreground_color = (self.foreground_color + 1) % len(COLORS)
        glColor4f(*COLORS[self.foreground_color])
    
    @q
    def cycleBackgroundColor(self):
        self.background_color = (self.background_color + 1) % len(COLORS)
        glClearColor(*COLORS[self.background_color])
    
    @q    
    def togglePerspective(self, width, height):
        self.orthogonal = not self.orthogonal
        self.reshape(width, height)
