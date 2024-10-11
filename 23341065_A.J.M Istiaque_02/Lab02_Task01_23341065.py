from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time

play = True
score = 0
diamond_x = random.randint(-250, 230)
diamond_y = 210
catcher_pos = [-90, -240]
catcher_clr = (1, 1, 1)
diamond_clr = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
cmp = 0.008
catcher_speed = 1
start_time = time.time()
last_time = start_time


def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def specialKeyListener(key, x, y):
    if diamond_y < -220: return
    if play and key == GLUT_KEY_LEFT and catcher_pos[0] > -250:
        catcher_pos[0] = max(catcher_pos[0] - 20 * catcher_speed, -250)
    elif play and key == GLUT_KEY_RIGHT and catcher_pos[0] + 160 < 250:
        catcher_pos[0] = min(catcher_pos[0] + 20 * catcher_speed, 90)
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global play, score, diamond_x, diamond_y, catcher_pos, catcher_clr, diamond_clr, cmp, catcher_speed, start_time, last_time
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # print("press", x, y)
        if x <= 60 and y <= 70:
            print("Starting Over!")
            play = True
            score = 0
            diamond_x = random.randint(-250, 230)
            diamond_y = 210
            catcher_pos = [-90, -240]
            catcher_clr = (1, 1, 1)
            diamond_clr = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
            cmp = 0.008
            catcher_speed = 1
            start_time = time.time()
            last_time = start_time
        elif 225 <= x <= 275 and y <= 70:
            play ^= True
        if x >= 440 and y <= 70:
            print(f"Goodbye! Score: {score}")
            glutLeaveMainLoop()
    glutPostRedisplay()


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx > 0 and dy >= 0:
        return abs(dx) <= abs(dy)
    elif dx <= 0 <= dy:
        return 2 if abs(dx) <= abs(dy) else 3
    elif dx < 0 and dy < 0:
        return 5 if abs(dx) <= abs(dy) else 4
    return 6 if abs(dx) <= abs(dy) else 7


def mid_point_line(x1, y1, x2, y2):
    ret = []
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * dy - 2 * dx
    x = x1
    y = y1
    for i in range(x, x2 + 1):
        ret.append([i, y])
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
    return ret


def convert_to_zero(zone, x, y):
    if zone == 1 or zone == 2 or zone == 5 or zone == 6:
        x, y = y, x
    if zone == 3 or zone == 4 or zone == 5 or zone == 6:
        x = -x
    if zone == 2 or zone == 4 or zone == 5 or zone == 7:
        y = -y
    return x, y


def convert_to_zoneM(clr, zone, points):
    glColor3f(*clr)
    if zone == 1 or zone == 2 or zone == 5 or zone == 6:
        for i in range(len(points)):
            points[i][0], points[i][1] = points[i][1], points[i][0]
    if zone == 2 or zone == 3 or zone == 4 or zone == 5:
        for i in range(len(points)):
            points[i][0] = -points[i][0]
    if zone == 4 or zone == 5 or zone == 6 or zone == 7:
        for i in range(len(points)):
            points[i][1] = -points[i][1]
    for x, y in points:
        draw_points(x, y, 3)


def draw_lines(clr, x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1, x2, y2 = *convert_to_zero(zone, x1, y1), *convert_to_zero(zone, x2, y2)
    points = mid_point_line(x1, y1, x2, y2)
    convert_to_zoneM(clr, zone, points)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    rgb = (0, 1, 1)
    draw_lines(rgb, -240, 225, -220, 240)
    draw_lines(rgb, -240, 225, -200, 225)
    draw_lines(rgb, -240, 225, -220, 210)

    rgb = (1, 1, 0)
    if play:
        draw_lines(rgb, -10, 240, -10, 210)
        draw_lines(rgb, 10, 240, 10, 210)
    else:
        draw_lines(rgb, -20, 240, 20, 225)
        draw_lines(rgb, -20, 240, -20, 210)
        draw_lines(rgb, -20, 210, 20, 225)

    rgb = (1, 0, 0)
    draw_lines(rgb, 200, 240, 240, 210)
    draw_lines(rgb, 200, 210, 240, 240)
    draw_lines(catcher_clr, catcher_pos[0], catcher_pos[1], catcher_pos[0] + 20, catcher_pos[1] - 15)
    draw_lines(catcher_clr, catcher_pos[0] + 20, catcher_pos[1] - 15, catcher_pos[0] + 140, catcher_pos[1] - 15)
    draw_lines(catcher_clr, catcher_pos[0] + 140, catcher_pos[1] - 15, catcher_pos[0] + 160, catcher_pos[1])
    draw_lines(catcher_clr, catcher_pos[0] + 160, catcher_pos[1], catcher_pos[0], catcher_pos[1])

    draw_lines(diamond_clr, diamond_x, diamond_y, diamond_x - 10, diamond_y - 10)
    draw_lines(diamond_clr, diamond_x - 10, diamond_y - 10, diamond_x, diamond_y - 20)
    draw_lines(diamond_clr, diamond_x, diamond_y - 20, diamond_x + 10, diamond_y - 10)
    draw_lines(diamond_clr, diamond_x + 10, diamond_y - 10, diamond_x, diamond_y)
    glutSwapBuffers()


def animate():
    global score, diamond_x, diamond_y, catcher_pos, catcher_clr, diamond_clr, start_time, last_time, cmp, catcher_speed
    if diamond_y == -220:
        if catcher_pos[0] - 20 < diamond_x < catcher_pos[0] + 160:
            score += 1
            diamond_x = random.randint(-250, 230)
            diamond_y = 210
            diamond_clr = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
            print(f"Score: {score}")
        else:
            catcher_clr = (1, 0, 0)
            print(f"Game Over! Score: {score}")
    if play:
        curr_time = time.time()
        diff = curr_time - last_time
        if diff >= cmp:
            diamond_y -= 1
            last_time = curr_time
        elapsed_time = curr_time - start_time
        if elapsed_time >= 8:
            cmp /= 1.5
            catcher_speed = min(catcher_speed + 1, 8)
            start_time = curr_time
    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(500, 800)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Catch the Diamonds!")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
