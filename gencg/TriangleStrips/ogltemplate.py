from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array
import sys, math, os
EXIT = -1
FIRST = 0
TRIANGLE_STRIP = []

def init(width, height):
    """ Initialize an OpenGL window """
    glClearColor(0.0, 0.0, 1.0, 0.0)         #background color
    glMatrixMode(GL_PROJECTION)              #switch to projection matrix
    glLoadIdentity()                         #set to 1
    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0) #multiply with new p-matrix
    glMatrixMode(GL_MODELVIEW)               #switch to modelview matrix


def display():
    """ Render all objects"""
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.75, 0.75, 0.75)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    TRIANGLE_STRIP.bind()
    glVertexPointerf(TRIANGLE_STRIP)
    glEnableClientState(GL_VERTEX_ARRAY)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, len(TRIANGLE_STRIP))
    TRIANGLE_STRIP.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    
    glFlush()

def renderTriangleStrip():
    pass

def renderTriangles():
    pass
def reshape(width, height):
    """ adjust projection matrix to window size"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width <= height:
        glOrtho(-1.5, 1.5,
                -1.5*height/width, 1.5*height/width,
                -1.0, 1.0)
    else:
        glOrtho(-1.5*width/height, 1.5*width/height,
                -1.5, 1.5,
                -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def keyPressed(key, x, y):
    """ handle keypress events """
    if key == chr(27): # chr(27) = ESCAPE
        sys.exit()


def mouse(button, state, x, y):
    """ handle mouse events """
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print "left mouse button pressed at ", x, y


def mouseMotion(x,y):
       """ handle mouse motion """
       print "mouse motion at ", x, y


def menu_func(value):
    """ handle menue selection """
    print "menue entry ", value, "choosen..."
    if value == EXIT:
        sys.exit()
    glutPostRedisplay()

def parse_trianglestrip():
    global TRIANGLE_STRIP
    strip = []
    
    for line in file('triangles.strip'):
        coords = line.split(':')[1]
        coords = [float(t) for t in coords.strip().split()]
        strip.append(coords)
        
    maxValue = max([max(t) for t in strip])
    strip = [[1 - x*2  / maxValue for x in t]for t in strip]
    TRIANGLE_STRIP = vbo.VBO(array(strip,'f'))
    
    
def main():
    # Hack for Mac OS X
    cwd = os.getcwd()
    os.chdir(cwd)
    parse_trianglestrip()
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("simple openGL/GLUT template")
    
    glutDisplayFunc(display)     #register display function
    glutReshapeFunc(reshape)     #register reshape function
    glutKeyboardFunc(keyPressed) #register keyboard function 
    glutMouseFunc(mouse)         #register mouse function
    glutMotionFunc(mouseMotion)  #register motion function
    glutCreateMenu(menu_func)    #register menue function
    
    glutAddMenuEntry("First Entry",FIRST) #Add a menu entry
    glutAddMenuEntry("EXIT",EXIT)         #Add another menu entry
    glutAttachMenu(GLUT_RIGHT_BUTTON)     #Attach mouse button to menue
    
    init(500,500) #initialize OpenGL state
    
    glutMainLoop() #start even processing


if __name__ == "__main__":
    main()
