import math, random, time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

play = True
score = 0
bomb_blast = 0
bomb_lst = []
bomb_radius = 15
bomb_clr = (1, 0, 1)
bomb_speed = 10

shooter_pos = [0, -245]
shooter_radius = 10
shooter_clr = (1, 1, 1)
shooter_speed = 1

fire_lst = []
fire_radius = 5
misfire = 0

cmp = 0.15
cmp2 = 2
start_time = time.time()
last_time = start_time
last_time2 = start_time


def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def keyboardListener(key, x, y):
    if not play or shooter_clr[1] == 0: return
    if key == b' ':
        fire_lst.append(shooter_pos.copy())
    elif key == b'a':
        shooter_pos[0] = max(shooter_pos[0] - 25, -245)
    elif key == b'd':
        shooter_pos[0] = min(shooter_pos[0] + 25, 245)


def reset(x):
    global play, score, bomb_blast, bomb_lst, shooter_pos, shooter_clr, fire_lst, start_time, last_time, last_time2
    play = x
    score = 0
    bomb_blast = 0
    bomb_lst = []
    if x: shooter_pos = [0, -245]
    shooter_clr = (1, 1, 1) if x else (1, 0, 0)
    fire_lst = []
    start_time = time.time()
    last_time = start_time
    last_time2 = start_time


def mouseListener(button, state, x, y):
    global play
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # print("press", x, y)
        if x <= 90 and y <= 70:
            print("Starting Over!")
            reset(True)
        elif 365 <= x <= 435 and y <= 70:
            if shooter_clr[1] == 0:
                reset(True)
            else:
                play ^= True
        if x >= 710 and y <= 70:
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


def convert_to_zoneN(zone, x, y, x1, y1):
    if zone == 1 or zone == 2 or zone == 5 or zone == 6:
        x1, y1 = y1, x1
    if zone == 2 or zone == 3 or zone == 4 or zone == 5:
        x1 = -x1
    if zone == 4 or zone == 5 or zone == 6 or zone == 7:
        y1 = -y1
    draw_points(x + x1, y + y1, 2)


def draw_circle(clr, x, y, r):
    glColor3f(*clr)
    x1, y1 = 0, r
    d = 1 - r
    while x1 < y1:
        for i in range(8):
            convert_to_zoneN(i, x, y, x1, y1)
        if d > 0:
            d += 2 * x1 - 2 * y1 + 5
            x1 += 1
            y1 -= 1
        else:
            d += 2 * x1 + 3
            x1 += 1


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
    draw_points(256, 256, 5)

    draw_circle(shooter_clr, *shooter_pos, shooter_radius)
    for i in fire_lst:
        draw_circle(shooter_clr, *i, fire_radius)
    for i in bomb_lst:
        draw_circle(bomb_clr, *i, bomb_radius)
    glutSwapBuffers()


def collide(a, b, r1, r2):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) <= r1 + r2


def animate():
    global score, shooter_pos, shooter_clr, bomb_clr, start_time, last_time, cmp, shooter_speed, bomb_blast, last_time2, misfire
    for i in bomb_lst:
        if collide(shooter_pos, i, shooter_radius, bomb_radius):
            print(f"Game Over! Score: {score}")
            reset(False)
            break
        for j in fire_lst:
            if collide(i, j, bomb_radius, fire_radius):
                score += 1
                print(f"Score: {score}")
                bomb_lst.remove(i)
                fire_lst.remove(j)
                break
        else:
            if i[1] < -250:
                bomb_blast += 1
                print(f"Missed: {bomb_blast}")
                bomb_lst.remove(i)
                if bomb_blast >= 3:
                    print(f"Game Over! Score: {score}")
                    reset(False)
                    break

    if play:
        for i in fire_lst:
            i[1] += 1
            if i[1] > 250:
                misfire += 1
                print(f"Misfire: {misfire}")
                fire_lst.remove(i)
            if misfire >= 3:
                print(f"Game Over! Score: {score}")
                reset(False)
                break

        curr_time = time.time()
        diff = curr_time - last_time
        if diff >= cmp:
            for i in bomb_lst: i[1] -= bomb_speed
            for i in fire_lst: i[1] += 1
            last_time = curr_time

        diff = curr_time - last_time2
        if diff > 1:
            new_bomb = [random.randint(-240, 240), 245]
            while True:
                f = True
                for i in bomb_lst:
                    if collide(new_bomb, i, bomb_radius, bomb_radius):
                        f = False
                        break
                if f: break
                new_bomb = [random.randint(-240, 240), 245]
            bomb_lst.append(new_bomb)
            last_time2 = curr_time
    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Circle Shooter Game!")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
