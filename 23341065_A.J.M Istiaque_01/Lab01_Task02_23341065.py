import random, time

from OpenGL.GL import *
from OpenGL.GLUT import *

freeze, blink = False, False
tmp_curr_time, tmp_blink = None, None
curr_time = 1000
blink_time = 0
xmax, xmin, ymax, ymin = None, None, None, None
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
    if curr_time != -1:
        glutTimerFunc(curr_time, update, None)


def keyboardListener(key, x, y):
    global curr_time
    if key == GLUT_KEY_UP:
        curr_time = max(0, curr_time - 50)
    elif key == GLUT_KEY_DOWN:
        curr_time += 50


def keyboardListener2(key, x, y):
    global freeze, curr_time, blink, tmp_curr_time, tmp_blink
    if key == b' ':
        if freeze:
            freeze = False
            curr_time, blink = tmp_curr_time, tmp_blink
            glutTimerFunc(curr_time, update, None)

        else:
            freeze = True
            tmp_curr_time, tmp_blink = curr_time, blink
            curr_time = -1
            blink = False
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global blink, blink_time
    if button == GLUT_RIGHT_BUTTON:
        calc_region(x, y)
    elif button == GLUT_LEFT_BUTTON:
        blink = True
        blink_time = time.time()
    glutPostRedisplay()


def display():
    global blink_time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if xmax != None:
        draw_region()
        diff = (time.time() - blink_time) % 2
        if not blink or diff <= 1 or freeze:
            for x, y, r, g, b, d in points:
                draw_point(x, y, r, g, b)
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Task 2: Building the Amazing Box")

init()
glutDisplayFunc(display)
glutTimerFunc(curr_time, update, None)
glutMouseFunc(mouseListener)
glutSpecialFunc(keyboardListener)
glutKeyboardFunc(keyboardListener2)
glutMainLoop()
