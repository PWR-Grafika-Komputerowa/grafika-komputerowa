#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *

ITERATION_LEVEL = 3


def is_in_sierpinski_carpet(i, j):

    while i > 0 or j > 0:

        if i % 3 == 1 and j % 3 == 1:
            return False
        i //= 3
        j //= 3
    return True


def draw_sierpinski_carpet_iterative(x, y, a, b, level):

    grid_size = 3 ** level

    dx = a / grid_size
    dy = b / grid_size

    x0 = x - a / 2.0
    y0 = y - b / 2.0

    glBegin(GL_TRIANGLES)

    for i in range(grid_size):
        for j in range(grid_size):
            if is_in_sierpinski_carpet(i, j):
                px = x0 + i * dx
                py = y0 + j * dy

                #Pierwszy trójkat
                glColor3f(0.8, 0.2, 0.2)
                glVertex2f(px, py)
                glVertex2f(px + dx, py)
                glVertex2f(px + dx, py + dy)

                # Drugi trójkąt
                glColor3f(0.2, 0.4, 0.8)
                glVertex2f(px, py)
                glVertex2f(px + dx, py + dy)
                glVertex2f(px, py + dy)

    glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.15, 0.15, 0.15, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    draw_sierpinski_carpet_iterative(0.0, 0.0, 160.0, 160.0, ITERATION_LEVEL)

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

    window = glfwCreateWindow(600, 600, "Dywan Sierpińskiego - Iteracyjny", None, None)
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