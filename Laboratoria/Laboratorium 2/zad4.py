#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def draw_rectangle(x, y, a, b):

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)

    glVertex2f(x, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)
    glEnd()


def draw_sierpinski_carpet(x, y, a, b, depth):

    if depth == 0:
        glColor3f(1.0, 0.0, 0.0)
        draw_rectangle(x, y, a, b)
    else:
        da = a / 3.0
        db = b / 3.0
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                draw_sierpinski_carpet(x + i * da, y + j * db, da, db, depth - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    recursion_depth = 3

    draw_sierpinski_carpet(-80.0, -80.0, 160.0, 160.0, recursion_depth)

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