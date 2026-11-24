#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup(window):
    width, height = glfwGetFramebufferSize(window)
    update_viewport(window, width, height)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def draw_rectangle(x, y, a, b):
    half_a = a / 2.0
    half_b = b / 2.0

    ax, ay = x - half_a, y - half_b
    bx, by = x + half_a, y - half_b
    cx, cy = x + half_a, y + half_b
    dx, dy = x - half_a, y + half_b

    glBegin(GL_TRIANGLES)
    glVertex2f(ax, ay)
    glVertex2f(bx, by)
    glVertex2f(cx, cy)

    glVertex2f(ax, ay)
    glVertex2f(cx, cy)
    glVertex2f(dx, dy)
    glEnd()




def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.5, 1.0)

    draw_rectangle(0.0, 0.0, 80.0, 40.0)

    glFlush()


def update_viewport(window, width, height):
    print("viewport:", width, height)
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