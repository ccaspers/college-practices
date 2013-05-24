from Tkinter import *
from Canvas import *
import numpy as np

WIDTH = 700  # width of canvas
HEIGHT = 700  # height of canvas

HPSIZE = 3  # half of point size (must be integer)
CLSIZE = 4  # line size
FCOLOR = "#000000"  # black (fill color)
BCOLOR = "#000000"  # blue (boundary color)

EPSILON = 0.000001

testPoints = False
numPolyPoints = 0

pointList = []  # list of points
elementList = []  # list of elements (used by Canvas.delete(...))


def intersect(line1, line2):
    line1Hom = convertToHomVec(line1)
    line2Hom = convertToHomVec(line2)

    point = intersectionPoint(line1Hom, line2Hom)
    xS = point[0]
    minX1, maxX1 = min(line1[0][0], line1[1][0]), max(line1[0][0], line1[1][0])
    xP = min(line2[0][0], line2[1][0])

    if minX1 < point[0] <= maxX1 and xP <= xS:
        return True
    return False

def convertToHomVec(line):
    p1 = np.array(tuple(line[0][:2]) + (1,), np.float)
    p2 = np.array(tuple(line[1][:2]) + (1,), np.float)
    cross = np.cross(p1, p2)
    return cross


def intersectionPoint(line1, line2):
    intersection = np.cross(line1, line2)
    intersection = intersection / intersection[2]
    return (intersection[0], intersection[1])


def pointInPolygon(p):
    """ test wether point p is in polygon pointList[:numPolyPoints] or not"""
    pList = pointList[:numPolyPoints]
    pList.append(pointList[0])
    count = 0
    testLine = [p, [WIDTH, p[1]]]
    for line in zip(pList, pList[1:]):
        if intersect(line, testLine):
            count = count + 1
    return (count % 2) == 1


def drawPoints():
    """ draw points """
    for p in pointList:
        if p[2]:  # flag wether point is in polygon or not
            fillColor = FCOLOR
        else:
            fillColor = ''
        element = can.create_oval(p[0] - HPSIZE, p[1] - HPSIZE,
                                  p[0] + HPSIZE, p[1] + HPSIZE,
                                  fill=fillColor, outline=BCOLOR)
        elementList.append(element)


def drawPolygon():
    """ use first numPolyPoints points in pointlist to draw a polygon"""
    pList = [[x, y] for [x, y, z] in pointList[:numPolyPoints]]
    element = can.create_polygon(pList, fill='#AAAAAA', outline='black', width=3)
    elementList.append(element)


def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPolygon()
    drawPoints()


def switchOnTest():
    """ switch on test mode """
    global testPoints
    testPoints = True


def clearAll():
    """ clear all (point list and canvas) """
    global testPoints
    testPoints = False
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    # get point coordinates Last entry
    # True if p is in Polygon False otherwise
    testPoint(event.x, event.y)
    draw()

def testPoint(x, y):
    global numPolyPoints
    p = [x, y, True]
    pointList.append(p)
    if not testPoints:  # append to polygon
        numPolyPoints = len(pointList)
    else:  # test wether point is in polygon or not
        p[2] = pointInPolygon(p)
        
def autoTest():
    switchOnTest()
    for x in range(0, WIDTH, 10):
        for y in range(0, HEIGHT, 10):
            testPoint(x, y)
    draw()

if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 1:
        print "Test in point is in (nonconvex) polygon"
        sys.exit(-1)

    # create main window
    mw = Tk()
    mw._root().wm_title("Point in (nonconvex) polygon test")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>", mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    bTest = Button(cFr, text="Test points", command=switchOnTest)
    bTest.pack(side="left")
    bAutoTest = Button(cFr, text="Autotest", command=autoTest)
    bAutoTest.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # start
    mw.mainloop()
