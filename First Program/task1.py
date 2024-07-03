from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

now = 0
bg_color= 1
rain_drops = [[random.uniform(-1, 1), random.uniform(0, 1)] for i in range(150)]

def init():
    glClearColor(bg_color, bg_color, bg_color, 0)
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)

def draw_roof():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.5, 0.0)
    glVertex2f(0.0, 0.5)
    glVertex2f(0.5, 0.0)
    glEnd()

def draw_walls():
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.49, 0.0)
    glVertex2f(-0.49, -0.8)
    glVertex2f(-0.49, -0.8)
    glVertex2f(0.49, -0.8)
    glVertex2f(0.49, -0.8)
    glVertex2f(0.49, 0.0)
    glEnd()

def draw_door():
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

def draw_door_lock():
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex2f(-0.25, -0.55)
    glEnd()

def draw_window():
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

def draw_rain_drops():
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    for x1, y1 in rain_drops:
        x2 = x1 + now
        y2 = y1 - 0.05
        y_actual1 = lambda x: x + 0.5
        y_actual2 = lambda x: -x + 0.5
        if (-0.5 <= x2 <= 0.5 or -0.5 <= x1 <= 0.5) and (y2 <= y_actual1(x2) if x2 <= 0 else y2 <= y_actual2(x2)):
            continue
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_roof()
    draw_walls()
    draw_door()
    draw_door_lock()
    draw_window()
    draw_rain_drops()
    glutSwapBuffers()


def update(val):
    assert -0.1 < now < 0.1
    for i in rain_drops:
        i[0] += now
        i[1] -= 0.01 + abs(now)
        if i[1] < -1:
            i[0] = random.uniform(-1, 1)
            i[1] = random.uniform(0, 1)
    glutPostRedisplay()
    glutTimerFunc(25, update, None)


def keyboardListener(key, x, y):
    global now, bg_color
    if key == GLUT_KEY_LEFT:
        now -= 0.001
    elif key == GLUT_KEY_RIGHT:
        now += 0.001
    if key == GLUT_KEY_UP: #light to dark
        bg_color = max(0, bg_color-0.1)
    elif key == GLUT_KEY_DOWN: #dark to light
        bg_color = min(1, bg_color+0.1)
    init()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(700, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Task 1: Building a House in Rainfall")

init()
glutDisplayFunc(display)
glutTimerFunc(25, update, None)
glutSpecialFunc(keyboardListener)
glutMainLoop()
