#!/usr/bin/env python3
import sys
import math
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

RANDOM_SEED = random.randint(0, 1000000)


def startup():

    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_deformed_rectangle(x, y, a, b, d=0.0):

    deformed_a = a * (1.0 + random.uniform(-d, d))
    deformed_b = b * (1.0 + random.uniform(-d, d))

    glColor3f(random.random(), random.random(), random.random())

    glBegin(GL_TRIANGLES)

    glVertex2f(x, y)
    glVertex2f(x + deformed_a, y)
    glVertex2f(x + deformed_a, y + deformed_b)

    glVertex2f(x, y)
    glVertex2f(x + deformed_a, y + deformed_b)
    glVertex2f(x, y + deformed_b)

    glEnd()


def render(time):
    random.seed(RANDOM_SEED)
    glClear(GL_COLOR_BUFFER_BIT)
    draw_deformed_rectangle(-50.0, -30.0, 100.0, 60.0, d=0.3)
    glFlush()

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
        glfwWaitEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()