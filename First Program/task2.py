import random

from OpenGL.GL import *
from OpenGL.GLUT import *

state = True
xmax, xmin, ymax, ymin = None, None, None, None
time = 1000
diag = [(-000.1, 000.1), (000.1, -000.1), (000.1, 000.1), (-000.1, -000.1)]
change_diag = [1, 0, 3, 2]
points = []


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)


def calc_region(x, y):
    global xmax, xmin, ymax, ymin, points
    w = glutGet(GLUT_WINDOW_WIDTH) / 2
    h = glutGet(GLUT_WINDOW_HEIGHT) / 2
    converted_x = (x - w) / w
    converted_y = -((y - h) / h)
    xmax = min(1, converted_x + 0.4)
    xmin = max(-1, converted_x - 0.4)
    ymax = min(1, converted_y + 0.4)
    ymin = max(-1, converted_y - 0.4)
    points = [
        [random.uniform(xmin, xmax), random.uniform(ymin, ymax), random.uniform(0, 1), random.uniform(0, 1),
         random.uniform(0, 1),
         random.randint(0, 3)] for i in range(8)]


def draw_region():
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(xmax, ymin)
    glVertex2f(xmax, ymax)
    glVertex2f(xmax, ymax)
    glVertex2f(xmin, ymax)
    glVertex2f(xmin, ymax)
    glVertex2f(xmin, ymin)
    glVertex2f(xmin, ymin)
    glVertex2f(xmax, ymin)
    glEnd()


def draw_point(x, y, r, g, b):
    glPointSize(4)
    glBegin(GL_POINTS)
    glColor3f(r, g, b)
    glVertex2f(x, y)
    glEnd()


def update(val):
    for i in points:
        if not (xmin <= i[0] + diag[i[5]][0] <= xmax and ymin <= i[1] + diag[i[5]][1] <= ymax):
            i[5] = change_diag[i[5]]
        i[0] += diag[i[5]][0]
        i[1] += diag[i[5]][1]
    glutPostRedisplay()
    glutTimerFunc(time, update, None)


def keyboardListener(key, x, y):
    global time
    if key == GLUT_KEY_UP:
        time = max(0, time - 50)
    elif key == GLUT_KEY_DOWN:
        time += 50


def mouseListener(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON:
        calc_region(x, y)
        glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if xmax != None:
        draw_region()
        for x, y, r, g, b, d in points:
            draw_point(x, y, r, g, b)
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Task 1: Building a House in Rainfall")

init()
glutDisplayFunc(display)
glutTimerFunc(time, update, None)
glutMouseFunc(mouseListener)
glutSpecialFunc(keyboardListener)
glutMainLoop()
