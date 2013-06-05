#-*- coding: utf-8 -*-
'''
@author: Christian Caspers
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from model import Model

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
    
    def __init__(self, model, camera, width, height):
        self.model = model
        self.camera = camera
        self.foreground_color = COLORS.index(WHITE)
        self.background_color = COLORS.index(BLUE)
        self.orthogonal = True
        # Initialize the window
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glClearColor(*COLORS[self.background_color])
        glColor4f(*COLORS[self.foreground_color])
        self.reshape(width, width)
        

    def display(self):
        """ Render all objects"""
        glMatrixMode(GL_MODELVIEW)
        self.resetCurrentBuffer()
        self.renderModel()
        glutSwapBuffers()
        
    def resetCurrentBuffer(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    def updateCamera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        ex, ey, ez = self.camera.eye
        cx, cy, cz = self.camera.center
        ux, uy, uz = self.camera.up
        gluLookAt(ex, ey, ez,
                  cx, cy, cz,
                  ux, uy, uz)
        
    def renderModel(self):
        glPushMatrix()
        vbo = self.model.faces_vbo
        
        scale = self.model.scale
        glScale(scale, scale, scale)
        glTranslatef(*self.model.position)
        glMultMatrixf(self.model.getRotationMatrix())
        
        vbo.bind()
        glVertexPointerf(vbo)
        glEnableClientState(GL_VERTEX_ARRAY)
    
        glDrawArrays(GL_TRIANGLES, 0, len(vbo))
        
        glDisableClientState(GL_VERTEX_ARRAY)
        vbo.unbind()
        glPopMatrix()
    
    def reshape(self, width, height):
        """ adjust projection matrix to window size"""
        glMatrixMode(GL_PROJECTION)
        glViewport(0, 0, int(width), int(height))
        glLoadIdentity()
        if self.orthogonal:
            self.setupOrthogonalProjection(width, height)
        else:
            self.setupPerspectiveProjection(width, height)
            self.updateCamera()
    
    def setupOrthogonalProjection(self, width, height):
        aspect = float(width) / float(height)
        edge_length = Model.NORM_SIZE / 2
        z = self.camera.eye[2]
        if aspect <= 1:
            glOrtho(-edge_length, edge_length,
                    -edge_length / aspect, edge_length / aspect,
                    -z*2, z*2)
        else:
            glOrtho(-edge_length * aspect, edge_length* aspect,
                    -edge_length, edge_length,
                    -z*2, z*2)      
                  
    def setupPerspectiveProjection(self, width, height):
        aspect = float(width)/float(height)
        gluPerspective(self.camera.fov, aspect, 1.0, 100.0)
            
    def cycleForegroundColor(self):
        self.foreground_color = (self.foreground_color + 1) % len(COLORS)
        glColor4f(*COLORS[self.foreground_color])
    
    def cycleBackgroundColor(self):
        self.background_color = (self.background_color + 1) % len(COLORS)
        glClearColor(*COLORS[self.background_color])
        
    def togglePerspective(self, width, height):
        self.orthogonal = not self.orthogonal
        self.reshape(width, height)
