#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin,cos,pi
ZADANIE = "5_0"




viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0


# - - - - - - \
# Zmienne dodane na potrzeby zadan
# -------------\
phi = 0
delta_y = 0
mouse_y_pos_old = 0
right_mouse_button_pressed = 0
scale = 1.0
x_eye = 0.0
y_eye = 0.0
z_eye = 0.0
R =10
mode = "object"
sierpinski_depth = 3



def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


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


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    axes()
    example_object()

    glFlush()


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


# - - - - - -\
# Zad 3.0
# - --- - - - -\

def mouse_motion_callback_3_0(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def render_3_0(time):
    global theta, phi
    global delta_x, delta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    delta_x = delta_y = 0
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)
    axes()
    example_object()

    glFlush()

# - - - - - -\
# Zad 3.5
# - --- - - - -\

def mouse_button_callback_3_5(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT:
        left_mouse_button_pressed = 1 if action == GLFW_PRESS else 0

    if button == GLFW_MOUSE_BUTTON_RIGHT:
        right_mouse_button_pressed = 1 if action == GLFW_PRESS else 0

def render_3_5(time):
    global theta, phi, scale
    global delta_x, delta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        scale -= delta_y * 0.01
        scale = max(0.1, min(scale, 5.0))

    delta_x = delta_y = 0
    glRotatef(phi, 1.0, 0.0, 0.0)
    glRotatef(theta, 0.0, 1.0, 0.0)
    axes()
    glScalef(scale,scale,scale)
    example_object()

    glFlush()

# - - - - - -\
# Zad 4.0
# - --- - - - -\
def render_4_0(time):
    global R, theta, phi
    global delta_x, delta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        R += delta_y * 0.05
        R = max(3.0, min(R, 50.0))

    delta_x = delta_y = 0

    x_eye = R * cos(theta * pi / 180) * cos(phi * pi / 180)
    y_eye = R * sin(phi * pi / 180)
    z_eye = R * sin(theta * pi / 180) * cos(phi * pi / 180)

    gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

    axes()
    example_object()

    glFlush()
# - - - - - -\
# Zad 4.5
# - --- - - - -\
def keyboard_key_callback_4_5(window, key, scancode, action, mods):
    global mode

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        mode = "camera" if mode == "object" else "object"


def render_4_5(time):
    global R, theta, phi, scale
    global delta_x, delta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    theta %= 360.0
    phi %= 360.0

    if mode == "object":
        if right_mouse_button_pressed:
            scale -= delta_y * 0.01
            scale = max(0.1, min(scale, 5.0))

        delta_x = delta_y = 0

        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
        glRotatef(theta, 0.0, 1.0, 0.0)
        axes()
        glScalef(scale, scale, scale)
        example_object()

    else:
        if right_mouse_button_pressed:
            R += delta_y * 0.05
            R = max(3.0, min(R, 50.0))

        delta_x = delta_y = 0

        x_eye = R * cos(theta * pi / 180) * cos(phi * pi / 180)
        y_eye = R * sin(phi * pi / 180)
        z_eye = R * sin(theta * pi / 180) * cos(phi * pi / 180)

        up_y = -1.0 if 90.0 < phi < 270.0 else 1.0

        gluLookAt(x_eye, y_eye, z_eye,
                  0.0, 0.0, 0.0,
                  0.0, up_y, 0.0)

        axes()
        example_object()

    glFlush()

# - - - - - -\
# Zad 5.0 (Trojkat Sierpinskiego 3D
# - - - - - -/


TETRA = [
    [ 3.0,  3.0,  3.0],
    [-3.0, -3.0,  3.0],
    [-3.0,  3.0, -3.0],
    [ 3.0, -3.0, -3.0],
]

FACES = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
COLORS = [(1.0, 0.2, 0.2), (0.2, 1.0, 0.2), (0.2, 0.4, 1.0), (1.0, 1.0, 0.2)]


def midpoint(a, b):
    return [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2]


def draw_tetrahedron(p):
    glBegin(GL_TRIANGLES)
    for face, color in zip(FACES, COLORS):
        glColor3f(*color)
        for idx in face:
            glVertex3f(*p[idx])
    glEnd()


def sierpinski(p, depth):
    if depth == 0:
        draw_tetrahedron(p)
        return

    for i in range(4):
        smaller = [p[i] if j == i else midpoint(p[i], p[j]) for j in range(4)]
        sierpinski(smaller, depth - 1)


def keyboard_key_callback_5_0(window, key, scancode, action, mods):
    global sierpinski_depth

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        sierpinski_depth = min(sierpinski_depth + 1, 5)
    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        sierpinski_depth = max(sierpinski_depth - 1, 0)


def render_5_0(time):
    global R, theta, phi
    global delta_x, delta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    theta %= 360.0
    phi %= 360.0

    if right_mouse_button_pressed:
        R += delta_y * 0.05
        R = max(0.5, min(R, 50.0))    

    delta_x = delta_y = 0

    x_eye = R * cos(theta * pi / 180) * cos(phi * pi / 180)
    y_eye = R * sin(phi * pi / 180)
    z_eye = R * sin(theta * pi / 180) * cos(phi * pi / 180)

    up_y = -1.0 if 90.0 < phi < 270.0 else 1.0

    gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0,
              0.0, up_y, 0.0)

    axes()
    sierpinski(TETRA, sierpinski_depth)

    glFlush()

LISTA_zadan = {
    "orig": (render, keyboard_key_callback, mouse_motion_callback, mouse_button_callback),
    "3_0":  (render_3_0, keyboard_key_callback, mouse_motion_callback_3_0, mouse_button_callback),
    "3_5":  (render_3_5, keyboard_key_callback, mouse_motion_callback_3_0, mouse_button_callback_3_5),
    "4_0":  (render_4_0, keyboard_key_callback, mouse_motion_callback_3_0, mouse_button_callback_3_5),
    "4_5":  (render_4_5, keyboard_key_callback_4_5, mouse_motion_callback_3_0, mouse_button_callback_3_5),
    "5_0": (render_5_0, keyboard_key_callback_5_0, mouse_motion_callback_3_0, mouse_button_callback_3_5)
}


def main():
    render_fn, key_cb, motion_cb, button_cb = LISTA_zadan[ZADANIE]

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

    startup()
    while not glfwWindowShouldClose(window):
        render_fn(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
