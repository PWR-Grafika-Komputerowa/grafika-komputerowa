#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *

smooth = True


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def draw_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-90.0, 10.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-10.0, 10.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-50.0, 80.0)
    glEnd()


def draw_rectangle(x, y, a, b):
    hx, hy = a / 2, b / 2
    bl = (x - hx, y - hy)
    tl = (x - hx, y + hy)
    tr = (x + hx, y + hy)
    br = (x + hx, y - hy)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(*bl)
    glVertex2f(*tl)
    glVertex2f(*tr)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(*bl)
    glVertex2f(*tr)
    glVertex2f(*br)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glShadeModel(GL_SMOOTH if smooth else GL_FLAT)
    draw_triangle()
    draw_rectangle(50.0, 45.0, 70.0, 50.0)
    glFlush()


def keyboard_key_callback(window, key, scancode, action, mods):
    global smooth
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        smooth = not smooth
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
