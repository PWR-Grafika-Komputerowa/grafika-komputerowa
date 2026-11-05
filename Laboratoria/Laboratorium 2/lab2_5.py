#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

DEPTH = 5
SIZE = 160.0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def vertices():
    height = SIZE * math.sqrt(3.0) / 2.0
    return (
        (-SIZE / 2.0, -height / 3.0),
        (SIZE / 2.0, -height / 3.0),
        (0.0, 2.0 * height / 3.0),
    )


def midpoint(p, q):
    return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)


def triangle(v0, v1, v2, depth):
    if depth <= 0:
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(*v0)
        glVertex2f(*v1)
        glVertex2f(*v2)
        glEnd()
        return

    a = midpoint(v0, v1)
    b = midpoint(v1, v2)
    c = midpoint(v2, v0)
    triangle(v0, a, c, depth - 1)
    triangle(a, v1, b, depth - 1)
    triangle(c, b, v2, depth - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    v0, v1, v2 = vertices()
    triangle(v0, v1, v2, DEPTH)

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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0, 1.0, -1.0)

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


if __name__ == "__main__":
    main()
