#!/usr/bin/env python3

import sys

from glfw.GLFW import *
from OpenGL.GL import *
import random

def startup():
    glClearColor(0.0, 0.0, 0.0, 1.0)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_QUADS)
    fractal(-1.0, -1.0, 2.0, 5)
    glEnd()
    glFlush()

def fractal(x, y, s, d):
    if d == 0:
        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(x, y)
        glVertex2f(x + s, y)
        glVertex2f(x + s, y + s)
        glVertex2f(x, y + s)
        return

    m = s / 3.0

    for wiersz in range(3):
        for kolumna in range(3):
            if wiersz == 1 and kolumna == 1:
                continue

            fractal(x + wiersz * m, y + kolumna * m, m, d - 1)

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1500, 750, "Lab2fraktal", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)
    startup()

    while not glfwWindowShouldClose(window):
        render()
        glfwSwapBuffers(window)

    glfwTerminate()


if __name__ == '__main__':
    main()