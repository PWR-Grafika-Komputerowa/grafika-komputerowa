#!/usr/bin/env python3
import sys
import random
SEED = 0.0

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    global SEED
    SEED = random.random()

def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(SEED)

    draw_rectangle(-50.0, 50.0, 40.0, 40.0, 0.1)
    draw_rectangle(50.0, 50.0, 40.0, 40.0, 0.3)
    draw_rectangle(-50.0, -50.0, 40.0, 40.0, 0.7)
    draw_rectangle(50.0, -50.0, 40.0, 40.0, 1.0)

    draw_rectangle(0.0, 0.0, 30.0, 30.0)

    glFlush()

def draw_rectangle(x, y, a, b, d=0.0):

    c1 = (random.random(), random.random(), random.random())
    c2 = (random.random(), random.random(), random.random())
    c3 = (random.random(), random.random(), random.random())
    c4 = (random.random(), random.random(), random.random())

    s1 = random.uniform(-a/2 * d, a/2 * d)
    z1 = random.uniform(-b/2 * d, b/2 * d)
    s2 = random.uniform(-a/2 * d, a/2 * d)
    z2 = random.uniform(-b/2 * d, b/2 * d)
    s3 = random.uniform(-a/2 * d, a/2 * d)
    z3 = random.uniform(-b/2 * d, b/2 * d)
    s4 = random.uniform(-a/2 * d, a/2 * d)
    z4 = random.uniform(-b/2 * d, b/2 * d)

    glBegin(GL_TRIANGLES)
    glColor3f(*c1)
    glVertex2f(x + a/2  + s1, y + b/2 + z1)
    glColor3f(*c3)
    glVertex2f(x + a/2 + s3, y - b/2 + z3)
    glColor3f(*c4)
    glVertex2f(x - a/2 + s4, y - b/2 + z4)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(*c1)
    glVertex2f(x + a/2  + s1, y + b/2 + z1)
    glColor3f(*c2)
    glVertex2f(x - a/2 + s2, y + b/2 + z2)
    glColor3f(*c4)
    glVertex2f(x - a/2 + s4, y - b/2 + z4)
    glEnd()
    


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
