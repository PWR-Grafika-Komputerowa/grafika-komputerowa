#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin,cos,pi,sqrt


ZADANIE = "5_0"

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# -- - - - - - - -\
# Zmienne dodane na potrzeby zadan:
# - - - - - - - - -\
light1_ambient = [0.0, 0.1, 0.1, 1.0]
light1_diffuse = [0.0, 0.8, 0.8, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [0.0, 0.0, -10.0, 1.0]
selected = 0
phi = 0.0
delta_y = 0
mouse_y_pos_old = 0
R_light = 5.0
theta1 = 180.0
phi1 = 0.0
right_mouse_button_pressed = 0
N = 30
tab_egg = []
tab_egg_normals = []
show_normals = False



def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)



def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

# - -- - -  - - - - \
#   Zad 3.0
# - - - - - - - -\
def startup_3_0():
    startup()

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glEnable(GL_LIGHT1)
def shutdown():
    pass

# - - - - - - -- \
# Zad 3.5
# - - - - - - -- \
def keyboard_key_callback_3_5(window, key, scancode, action, mods):
    global selected

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_TAB and action == GLFW_PRESS:
        selected = (selected + 1) % 3
        print("Wybrana skladowa:", "RGB"[selected])

    if key in (GLFW_KEY_UP, GLFW_KEY_DOWN) and action in (GLFW_PRESS, GLFW_REPEAT):
        step = 0.1 if key == GLFW_KEY_UP else -0.1
        value = light_diffuse[selected] + step
        light_diffuse[selected] = round(max(0.0, min(value, 1.0)), 1)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        print("light_diffuse (R, G, B):", light_diffuse[:3])


# - - - - - - -- \
# Zad 4.0
# - - - - - - -- \

def mouse_motion_callback_4_0(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback_4_0(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT:
        left_mouse_button_pressed = 1 if action == GLFW_PRESS else 0

    if button == GLFW_MOUSE_BUTTON_RIGHT:
        right_mouse_button_pressed = 1 if action == GLFW_PRESS else 0


def place_light(light_id, th, ph):
    xs = R_light * cos(th * pi / 180) * cos(ph * pi / 180)
    ys = R_light * sin(ph * pi / 180)
    zs = R_light * sin(th * pi / 180) * cos(ph * pi / 180)

    glLightfv(light_id, GL_POSITION, [xs, ys, zs, 1.0])

    glPushMatrix()
    glTranslatef(xs, ys, zs)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glPopMatrix()


def render_4_0(time):
    global delta_x, delta_y
    global theta, phi, theta1, phi1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        theta1 += delta_x * pix2angle
        phi1 += delta_y * pix2angle

    delta_x = delta_y = 0

    place_light(GL_LIGHT0, theta, phi)
    place_light(GL_LIGHT1, theta1, phi1)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 20, 20)
    gluDeleteQuadric(quadric)

    glFlush()

# - - - - - - -- \
# Zad 4_5
# - - - - - - - - \
def egg_point(u, v):
    a = -90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u
    return (a * cos(pi*v),
            160*u**4 - 320*u**3 + 160*u**2 - 5,
            a * sin(pi*v))

def egg_normal(u,v):
    p = 450 * u ** 4 - 900 * u ** 3 + 810 * u ** 2 - 360 * u + 45
    q = 90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u

    xu = -p * cos(pi * v)
    xv = pi * q * sin(pi * v)
    yu = 640 * u ** 3 - 960 * u ** 2 + 320 * u
    yv = 0.0
    zu = -p * sin(pi * v)
    zv = -pi * q * cos(pi * v)

    nx = yu * zv - zu * yv
    ny = zu * xv - xu * zv
    nz = xu * yv - yu * xv

    length = sqrt(nx * nx + ny * ny + nz * nz)
    if length < 1e-9:
        if u < 0.25 or u > 0.75:
            return (0.0, -1.0, 0.0)
        return (0.0, 1.0, 0.0)
    return (nx / length, ny / length, nz / length)

def startup_4_5():
    startup_3_0()
    tab_egg.clear()
    tab_egg_normals.clear()
    for i in range(N):
        u = i / (N - 1)
        row_p = []
        row_n = []
        for j in range(N):
            v = j / (N - 1)
            row_p.append(egg_point(u, v))
            row_n.append(egg_normal(u, v))
        tab_egg.append(row_p)
        tab_egg_normals.append(row_n)

def render_4_5(time):
    global theta
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3fv(tab_egg_normals[i][j])
            glVertex3fv(tab_egg[i][j])

            glNormal3fv(tab_egg_normals[i + 1][j])
            glVertex3fv(tab_egg[i + 1][j])
        glEnd()

    glFlush()

# - - - - - - - \
# Zad 5_0
# - - - - - - - \
def startup_5_0():
    startup_3_0()
    tab_egg.clear()
    tab_egg_normals.clear()
    for i in range(N):
        u = i / (N - 1)
        row_p = []
        row_n = []
        for j in range(N):
            v = j / (N - 1)
            n = egg_normal(u, v)
            if u > 0.5 and i != N - 1:
                n = (-n[0], -n[1], -n[2])
            row_p.append(egg_point(u, v))
            row_n.append(n)
        tab_egg.append(row_p)
        tab_egg_normals.append(row_n)

def keyboard_key_callback_5_0(window, key, scancode, action, mods):
    global show_normals

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_N and action == GLFW_PRESS:
        show_normals = not show_normals

def render_5_0(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3fv(tab_egg_normals[i][j])
            glVertex3fv(tab_egg[i][j])

            glNormal3fv(tab_egg_normals[i + 1][j])
            glVertex3fv(tab_egg[i + 1][j])
        glEnd()

    if show_normals:
        glDisable(GL_LIGHTING)
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                px, py, pz = tab_egg[i][j]
                nx, ny, nz = tab_egg_normals[i][j]
                glVertex3f(px, py, pz)
                glVertex3f(px + nx, py + ny, pz + nz)
        glEnd()
        glEnable(GL_LIGHTING)

    glFlush()


LISTA_zadan = {
    "orig": (startup,     render,     keyboard_key_callback,     mouse_motion_callback,     mouse_button_callback),
    "3_0":  (startup_3_0, render,     keyboard_key_callback,     mouse_motion_callback,     mouse_button_callback),
    "3_5":  (startup_3_0, render,     keyboard_key_callback_3_5, mouse_motion_callback,     mouse_button_callback),
    "4_0":  (startup_3_0, render_4_0, keyboard_key_callback,     mouse_motion_callback_4_0, mouse_button_callback_4_0),
    "4_5": (startup_4_5, render_4_5, keyboard_key_callback, mouse_motion_callback, mouse_button_callback),
    "5_0": (startup_5_0, render_5_0, keyboard_key_callback_5_0, mouse_motion_callback, mouse_button_callback),
}



def main():
    startup_fn, render_fn, key_cb, motion_cb, button_cb = LISTA_zadan[ZADANIE]

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, key_cb)
    glfwSetCursorPosCallback(window, motion_cb)
    glfwSetMouseButtonCallback(window, button_cb)
    glfwSwapInterval(1)

    startup_fn()
    while not glfwWindowShouldClose(window):
        render_fn(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()