from OpenGL.GL import *             # @UnusedWildImport
from OpenGL.GLUT import *           # @UnusedWildImport
from OpenGL.GL.shaders import *     # @UnusedWildImport
from math import *                  # @UnusedWildImport
from numpy import *                 # @UnusedWildImport
from numpy.linalg.linalg import inv

matrixStack = []
default_program = None

IDENTITY_MATRIX = matrix([
                  [1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]
                  ], dtype="f")


pMatrix = matrix.copy(IDENTITY_MATRIX)
mvMatrix = matrix.copy(IDENTITY_MATRIX)

mode = GL_PROJECTION

vertexShader = None
fragmentShader = None
active_program = None

def init():
    global default_program, vertexShader, fragmentShader
    vertexString = ''.join(file('assets/shader/gouraud.vert').readlines())
    fragmentString = ''.join(file('assets/shader/gouraud.frag').readlines())
    vertexShader = compileShader(vertexString, GL_VERTEX_SHADER)
    fragmentShader = compileShader(fragmentString, GL_FRAGMENT_SHADER)
    default_program = compileProgram(vertexShader, fragmentShader)
    useDefaultShaders()


def useProgram(program):
    global pMatrix, mvMatrix, active_program
    active_program = program
    glUseProgram(program)


def useDefaultShaders():
    useProgram(default_program)


def matrixMode(matrixmode):
    global mode
    allowed_modes = [GL_PROJECTION, GL_MODELVIEW]
    if matrixmode in allowed_modes:
        mode = matrixmode
    else:
        raise Exception("Wrong matrixmode chosen - GL_PROJECTION or GL_MODELVIEW allowed")


def loadIdentity():
    global pMatrix, mvMatrix
    if mode == GL_PROJECTION:
        pMatrix = matrix.copy(IDENTITY_MATRIX)
    elif mode == GL_MODELVIEW:
        mvMatrix = matrix.copy(IDENTITY_MATRIX)


def multMatrix(tmp):
    global pMatrix, mvMatrix
    if mode == GL_PROJECTION:
        pMatrix *= tmp
    elif mode == GL_MODELVIEW:
        mvMatrix *= tmp
    
    inMatrix = inv(mvMatrix[0:3, 0:3]).T
    mvpMatrix = pMatrix * mvMatrix
    
    sendMatrix4("mvMatrix", mvMatrix)
    sendMatrix4("mvpMatrix", mvpMatrix)
    sendMatrix3("normalMatrix", inMatrix)


def pushMatrix():
    matrixStack.append(matrix.copy(_active_matrix()))


def popMatrix():
    global pMatrix, mvMatrix
    newMatrix = matrixStack.pop()
    
    if mode == GL_PROJECTION:
        pMatrix = newMatrix
    elif mode == GL_MODELVIEW:
        mvMatrix = newMatrix


def _active_matrix():
    global pMatrix, mvMatrix
    if mode == GL_PROJECTION:
        return pMatrix
    elif mode == GL_MODELVIEW:
        return mvMatrix


def rotate(angle, axis):
    c, mc = cos(float(angle)), 1 - cos(float(angle))
    s = sin(angle)
    l = sqrt(dot(array(axis), array(axis)))
    x, y, z = array(axis) / l
    r = matrix(
            [
             [x*x*mc + c,    x*y*mc - z*s, x*z*mc + y*s,  0],
             [x*y*mc + z*s,  y*y*mc + c,   y*z*mc - x*s,  0],
             [x*z*mc - y*s,  y*z*mc + x*s, z*z*mc + c,    0],
             [0,             0,            0,             1]
            ], dtype="f"
        )
    multMatrix(r)

    
def scale(sx, sy, sz):
    tmp = matrix([[sx, 0, 0, 0],
                  [0, sy, 0, 0],
                  [0, 0, sz, 0],
                  [0, 0,  0, 1]
                  ], dtype="f")
    multMatrix(tmp)


def translate(tx, ty, tz):
    tmp = matrix([[ 1, 0, 0, tx],
                  [ 0, 1, 0, ty],
                  [ 0, 0, 1, tz],
                  [ 0, 0, 0,  1]
                ], dtype="f")
    multMatrix(tmp)


def lookAt(ex, ey, ez, cx, cy, cz, ux, uy, uz):
    e =  array([ex, ey, ez], dtype="f")
    c =  array([cx, cy, cz], dtype="f")
    up = array([ux, uy, uz], dtype="f")

    lup = sqrt(dot(up, up))
    up = up / lup

    f = c - e
    lf = sqrt(dot(f, f))
    f = f / lf

    s = cross(f, up)
    ls = sqrt(dot(s, s))
    s = s / ls

    u = cross(s, f)

    tmp = matrix([
                  [ s[0],  s[1],  s[2], -dot(s, e)],
                  [ u[0],  u[1],  u[2], -dot(u, e)],
                  [-f[0], -f[1], -f[2],  dot(f, e)],
                  [    0,     0,     0,          1]
                 ], dtype="f")
    multMatrix(tmp)


def perspective(fovy,aspect,zNear,zFar):
    """EntsprichtgluPerspective(fovy,aspect,zNear,zFar)"""
    f = 1.0 / tan(fovy / 2.0)
    aspect = float(aspect)
    zNear = float(zNear)
    zFar = float(zFar)
    p = matrix([
                [f / aspect, 0,                         0,                           0],
                [         0, f,                         0,                           0],
                [         0, 0, (zFar+zNear)/(zNear-zFar), (2*zFar*zNear)/(zNear-zFar)],
                [         0, 0,                        -1,                           0]
               ], dtype="f")
    multMatrix(p)
    
# TODO: effizienter machen -> varLocation vorher
# speichern und dann nur noch glUniform..(varLoc, val) setzen
def sendValue(varName, value):
    varLocation = glGetUniformLocation(active_program, varName)
    glUniform1f(varLocation, value)


def sendVec3(varName, value):
    varLocation = glGetUniformLocation(active_program, varName)
    glUniform3f(varLocation, *value)


def sendVec4(varName, value):
    varLocation = glGetUniformLocation(active_program, varName)
    glUniform4f(varLocation, *value)


def sendMatrix3(varName, matrix):
    varLocation = glGetUniformLocation(active_program, varName)
    glUniformMatrix3fv(varLocation, 1, GL_TRUE, matrix.tolist())


def sendMatrix4(varName, matrix):
    varLocation = glGetUniformLocation(active_program, varName)
    glUniformMatrix4fv(varLocation, 1, GL_TRUE, matrix.tolist())
