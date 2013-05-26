from OpenGL.GL import *
from OpenGL.GLUT import *
import sys, math

def initGL(width, height):
    glClearColor(0.0, 0.0, 1.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.75, 0.75, 0.75)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    for i in range(6):
        glVertex2f(math.cos( i*math.pi / 3),
                   math.sin( i*math.pi / 3))
    glEnd()
    glFlush()
    
def main():
    glutInit(sys.argv)
    print "INIT"
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    print "INITWINDOW"
    glutInitWindowSize(500, 500)
    print "CREATEWINDOW"
    glutCreateWindow("EasyCheesy")
    print "DISPLAYFUNC"
    glutDisplayFunc(display)
    print "INITGL"
    initGL(500, 500)
    glutMainLoop()
    
if __name__ == "__main__":
    main()
        