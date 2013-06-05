#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Viewer for OBJ-Files in WaveFront-OBJ-Format
Shows Wireframes, uses Open-GL

Creates objects, needed for rendering and reacts to user-input

@author: Christian Caspers
'''
from OpenGL.GL import *
from OpenGL.GLUT import *
from camera import Camera
from functools import wraps
from renderer import Renderer
import math
import model as modellib
import numpy as np

WIDTH, HEIGHT = 500, 500
KEY_ESCAPE = chr(27)

X_AXIS = (1.0, 0.0, 0.0)
Y_AXIS = (0.0, 1.0, 0.0)
Z_AXIS = (0.0, 0.0, 1.0)

AXIS = {'X':X_AXIS, 'Y':Y_AXIS, 'Z':Z_AXIS}

mouseX, mouseY, startP = None, None, None

def updateView(func):
    ''' masks the call to glutPostRedisplay '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        glutPostRedisplay()
    return wrapper


def mouseMotion(func):
    '''
    calclulates deltas for mouse-coords and caches the current ones
    each motion automatically triggers an update of the view
    '''
    @updateView
    @wraps(func)
    def wrapper(x, y):
        global mouseX, mouseY
        deltaX, deltaY = x - mouseX, mouseY - y 
        mouseX, mouseY = x, y
        func(deltaX, deltaY)
    return wrapper

@updateView
def keyPressed(key, x, y):
    angle = 2
    if key == KEY_ESCAPE:
        sys.exit()
    
    if key.upper() in "XYZ":
        angle = angle if key.isupper() else angle*-1
        angle = math.radians(angle)
        axis = AXIS[key.upper()]
        model.rotate(angle, axis)
        model.saveOrientation()

@updateView
def mouseClicked(button, state, x, y):
    ''' handle mouse events '''
    global mouseX, mouseY, startP
    if state == GLUT_DOWN:
        motionfuncs = {GLUT_LEFT_BUTTON  : rotateModel,
                       GLUT_MIDDLE_BUTTON: zoomModel,
                       GLUT_RIGHT_BUTTON : moveModel}
        startP = projectOnSphere(x, y)
        mouseX, mouseY = x, y
        if motionfuncs.get(button):
            glutMotionFunc(motionfuncs[button])
    else:
        model.saveOrientation()

@mouseMotion
def rotateModel(deltaX, deltaY):
    ''' handle mouse motion '''
    moveP = projectOnSphere(mouseX, mouseY)
    dotP = np.dot(startP, moveP)
    # if one is None, sth. is wrong
    if startP and moveP and dotP:
        angle = math.acos(dotP)
        axis = np.cross(startP, moveP)
        model.rotate(angle, axis)
    
def projectOnSphere(x, y):
    r = min(WIDTH, HEIGHT) / 2.0
    x, y = x-WIDTH/2.0, HEIGHT/2.0 - y
    a = min(r*r, x*y + y*y)
    z = math.sqrt(r*r - a)
    l = math.sqrt(x*x + y*y + z*z)
    return x/l, y/l, z/l

@mouseMotion
def zoomModel(deltaX,deltaY):
    length = math.sqrt(deltaX**2 + deltaY**2)
    mod = 1 if deltaY >= 0 else -1
    deltaZoom = length * mod / float(HEIGHT)
    model.adjustScale(deltaZoom)
    
@mouseMotion
def moveModel(deltaX, deltaY):
    move_factor = float(min(WIDTH, HEIGHT))
    mX = float(deltaX) / move_factor
    mY = float(deltaY) / move_factor
    model.move(mX, mY)

@updateView
def handleSpecialKeys(key, x, y):
    if key == GLUT_KEY_F1:
        oglRenderer.cycleBackgroundColor()
    elif key == GLUT_KEY_F2:
        oglRenderer.cycleForegroundColor()
    elif key == GLUT_KEY_F3:
        oglRenderer.togglePerspective(WIDTH, HEIGHT)

def reshape(width, height):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = width, height
    # Don't reshape if height or width is 0
    if WIDTH and HEIGHT:
        oglRenderer.reshape(WIDTH, HEIGHT)
    
def main(filename):
    global model, camera, oglRenderer
    applyOSXHack()
    initGlut()
    
    camera = Camera()
    model = modellib.parse(filename)
    oglRenderer = Renderer(model, camera, WIDTH, HEIGHT)
    registerCallbacks()
    glutMainLoop()

def initGlut():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("OBJ-Viewer - Christian Caspers")
    
def registerCallbacks():
    glutDisplayFunc(oglRenderer.display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouseClicked)
    glutSpecialFunc(handleSpecialKeys)

def applyOSXHack():
    cwd = os.getcwd()
    os.chdir(cwd)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python main.py PATH_TO_OBJ_FILE"
        sys.exit()
    main(sys.argv[1])
