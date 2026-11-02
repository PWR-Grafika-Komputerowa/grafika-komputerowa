#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
RECURSION_LEVEL = 3


def draw_rectangle(x, y, a, b, is_center=True):

    if is_center:
        x_min, x_max = x - a / 2.0, x + a / 2.0
        y_min, y_max = y - b / 2.0, y + b / 2.0
    else:
        x_min, x_max = x, x + a
        y_min, y_max = y, y + b

    glBegin(GL_TRIANGLES)

    # Pierwszy trójkąt
    glColor3f(0.8, 0.2, 0.2)
    glVertex2f(x_min, y_min)
    glVertex2f(x_max, y_min)
    glVertex2f(x_max, y_max)

    # Drugi trójkąt
    glColor3f(0.2, 0.4, 0.8)
    glVertex2f(x_min, y_min)
    glVertex2f(x_max, y_max)
    glVertex2f(x_min, y_max)

    glEnd()


def draw_sierpinski_carpet(x, y, a, b, level):

    if level == 0:
        draw_rectangle(x, y, a, b, is_center=True)
        return

    new_a = a / 3.0
    new_b = b / 3.0

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue

            sub_x = x + i * new_a
            sub_y = y + j * new_b

            draw_sierpinski_carpet(sub_x, sub_y, new_a, new_b, level - 1)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.2, 0.2, 0.2, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    draw_sierpinski_carpet(0.0, 0.0, 160.0, 160.0, RECURSION_LEVEL)

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

    window = glfwCreateWindow(600, 600, "Dywan Sierpińskiego", None, None)
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