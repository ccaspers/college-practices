from Canvas import *
from Tkinter import *
from camera import Camera
from model import Model
import model

WIDTH = 400         # width of canvas
HEIGHT = 400        # height of canvas

HPSIZE = 0.5        # radius of point
COLOR = "#0000FF"   # blue

pointList = []      # list of points (used by Canvas.delete(...))
modelObj = Model()
cam = Camera((0, 1, 0), (0, 0, 0), WIDTH, HEIGHT)

def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw points """
    points = cam.renderModel(modelObj).points
    for point in transformToWindowCoordinates(points):
        x, y = point
        p = can.create_oval(x - HPSIZE, y - HPSIZE, x + HPSIZE, y + HPSIZE,
                           fill=COLOR, outline=COLOR)
        pointList.insert(0, p)


def rotYp():
    """ rotate counterclockwise around y axis """
    rotateModel(10)


def rotYn():
    """ rotate clockwise around y axis """
    rotateModel(-10)


def rotateModel(angleInDegree):
    global modelObj, pointList
    can.delete(*pointList)
    pointList = []
    modelObj = modelObj.rotated(angleInDegree)
    draw()


def transformToWindowCoordinates(points):
    return [[t[0] * WIDTH / 2 + WIDTH / 2, t[1] * (-1) * HEIGHT / 2 + HEIGHT / 2] for t in points]

if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 2:
        print "pointViewerTemplate.py"
        sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    modelObj = model.parse(sys.argv[1]).normalized()
    cam.setupCameraForModel(modelObj)

    draw()
    # start
    mw.mainloop()
