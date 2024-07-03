from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

now = 0
raindrops = []
for i in range(150):
    x1= random.uniform(-1, 1)
    y1= random.uniform(0, 1)
    y2= y1- random.uniform(0.03,0.08)
    raindrops.append([x1,y1,y2])

def init():
    glClearColor(1.0, 1.0, 1.0, 0)
    glClearDepth(1.0)  # Depth Buffer Setup
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glDepthFunc(GL_LEQUAL)  # The Type Of Depth Testing To Do
    glShadeModel(GL_SMOOTH)  # Enables Smooth Shading
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-1, 1, -1, 1)  # Set up an orthographic projection matrix
    glMatrixMode(GL_MODELVIEW)


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # roof
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.5, 0.0)
    glVertex2f(0.0, 0.5)
    glVertex2f(0.5, 0.0)
    glEnd()

    # walls
    glLineWidth(1.5)
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.49, 0.0)
    glVertex2f(-0.49, -0.8)
    glVertex2f(-0.49, -0.8)
    glVertex2f(0.49, -0.8)
    glVertex2f(0.49, -0.8)
    glVertex2f(0.49, 0.0)
    glEnd()

    # door
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.4, -0.8)
    glVertex2f(-0.4, -0.3)
    glVertex2f(-0.4, -0.3)
    glVertex2f(-0.2, -0.3)
    glVertex2f(-0.2, -0.3)
    glVertex2f(-0.2, -0.8)
    glEnd()

    # door-lock
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex2f(-0.25, -0.55)
    glEnd()

    # window
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.1, -0.15)
    glVertex2f(0.3, -0.15)
    glVertex2f(0.3, -0.15)
    glVertex2f(0.3, -0.35)
    glVertex2f(0.3, -0.35)
    glVertex2f(0.1, -0.35)
    glVertex2f(0.1, -0.35)
    glVertex2f(0.1, -0.15)

    glVertex2f(0.2, -0.15)
    glVertex2f(0.2, -0.35)
    glVertex2f(0.1, -0.25)
    glVertex2f(0.3, -0.25)
    glEnd()

    # raindrops
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    for x1, y1, y2 in raindrops:
        x2= x1+now
        # y2= y1-0.05
        y_actual1 = lambda x: x + 0.5
        y_actual2 = lambda x: -x + 0.5
        if (-0.5 <= x2 <= 0.5 or -0.5<=x1<=0.5) and (y2 <= y_actual1(x2) if x2 <= 0 else y2 <= y_actual2(x2)):
            continue
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
    glEnd()

    glutSwapBuffers()


def update(val):
    assert -0.1<now<0.1
    for i in raindrops:
        i[0]+= now
        i[1] -= 0.01+abs(now)
        i[2] -= 0.01+abs(now)
        if i[1] < -1:
            i[0] = random.uniform(-1, 1)
            i[1] = random.uniform(0, 1)
            i[2]= i[1]- random.uniform(0.03,0.08)

    glutPostRedisplay()
    glutTimerFunc(25, update, None)

def keyboardListener(key, x, y):
    global now
    if key == GLUT_KEY_LEFT:
        now -= 0.001
    elif key == GLUT_KEY_RIGHT:
        now += 0.001

# Main function
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(700, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Task 1: Building a House in Rainfall")

init()
glutDisplayFunc(draw)
glutTimerFunc(20, update, None)
glutSpecialFunc(keyboardListener)
glutMainLoop()