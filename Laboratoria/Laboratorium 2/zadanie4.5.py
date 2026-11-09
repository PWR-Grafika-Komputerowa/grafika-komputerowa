#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


STOPIEN = 3


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def rysowanie_prostokata(x, y, a, b):
    hx = a / 2.0
    hy = b / 2.0

    bl = (x - hx, y - hy)
    tl = (x - hx, y + hy)
    tr = (x + hx, y + hy)
    br = (x + hx, y - hy)

    glColor3f(0.65, 0.25, 0.05)
    glBegin(GL_TRIANGLES)
    glVertex2f(*bl)
    glVertex2f(*br)
    glVertex2f(*tr)
    glVertex2f(*bl)
    glVertex2f(*tr)
    glVertex2f(*tl)
    glEnd()


def dywan_sierpinskiego(x, y, a, b, stopien):
    if stopien == 0:
        rysowanie_prostokata(x, y, a, b)
        return

    male_a = a / 3.0
    male_b = b / 3.0

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            dywan_sierpinskiego(x + i * male_a, y + j * male_b,
                                male_a, male_b, stopien - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    dywan_sierpinskiego(0.0, 0.0, 160.0, 160.0, STOPIEN)

    glFlush()


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
