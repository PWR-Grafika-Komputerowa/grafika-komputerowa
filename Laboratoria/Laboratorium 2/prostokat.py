#!/usr/bin/env python3

import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    rectangle(-0.5, -0.25, 1.0, 0.5, 0.15)
    glFlush()

def rectangle(x, y, a, b, d = 0.0):


    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + (random.random() * d), y + (random.random() * d))
    glVertex2f(x + a + (random.random() * d), y + (random.random() * d))
    glVertex2f(x + (random.random() * d), y + b + (random.random() * d))
    glEnd()

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + a + (random.random() * d), b + y + (random.random() * d))
    glVertex2f(x + a + (random.random() * d), y + (random.random() * d))
    glVertex2f(x + (random.random() * d), y + b + (random.random() * d))
    glEnd()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab2", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render()
        glfwSwapBuffers(window)
        glfwWaitEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()