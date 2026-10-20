#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

#losowanieeee
import random

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def rectangle(x, y, a, b, d=0.0):

    a = random.randrange(a, round(a * (1 + d)), 1)
    b = random.randrange(b, round(b * (1 + d)), 1)
    #x = random.rande(x, round(x * (1 + d)), 1)
    #y = random.randrange(y, round(y * (1 + d)), 1)


    r = random.randrange(0, round(100 * d), 1)
    g = random.randrange(0, round(100 * d), 1)
    bb = random.randrange(0, round(100 * d), 1)

    r /= 100
    g /= 100
    bb /= 100

    # TRÓJKĄT GÓRNY
    glColor3f(r, g, bb)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + b, y)
    glVertex2f(x, y - a)
    glEnd()

    # TRÓJKĄT DOLNY
    glColor3f((1 - r), (1 - g) , (1 - bb))
    glBegin(GL_TRIANGLES)
    glVertex2f(x + b, y - a)
    glVertex2f(x + b, y)
    glVertex2f(x, y - a)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # MIEJSCE NA KOD
    rectangle(-50,50,50,100, 0.5)

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

    random.seed()

    startup()
    while not glfwWindowShouldClose(window):

        render(1)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
