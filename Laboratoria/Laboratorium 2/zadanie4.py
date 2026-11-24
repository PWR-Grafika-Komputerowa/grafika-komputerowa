#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *



CARPET_COLOR = (0.55, 0.27, 0.07)


def startup(window):
    width, height = glfwGetFramebufferSize(window)
    update_viewport(window, width, height)
    glClearColor(1.0, 1.0, 1.0, 1.0)


def shutdown():
    pass


def draw_rectangle(x, y, a, b, color=CARPET_COLOR):

    half_a = a / 2.0
    half_b = b / 2.0

    ax, ay = x - half_a, y - half_b
    bx, by = x + half_a, y - half_b
    cx, cy = x + half_a, y + half_b
    dx, dy = x - half_a, y + half_b

    glColor3f(*color)
    glBegin(GL_TRIANGLES)

    glVertex2f(ax, ay)
    glVertex2f(bx, by)
    glVertex2f(cx, cy)

    glVertex2f(ax, ay)
    glVertex2f(cx, cy)
    glVertex2f(dx, dy)
    glEnd()


def draw_carpet(x, y, a, b, level):

    if level == 0:
        draw_rectangle(x, y, a, b)
        return

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            draw_carpet(x + i * a / 3, y + j * b / 3, a / 3, b / 3, level - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    LEVEL = 4

    draw_carpet(0.0, 0.0, 180.0, 120.0, LEVEL)

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

    startup(window)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()