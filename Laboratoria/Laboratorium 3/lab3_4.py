#!/usr/bin/env python3
import math
import sys
from random import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 20

tab = [[[0.0] * 3 for i in range(N)] for j in range(N)]
colors = [[[0.0] * 3 for i in range(N)] for j in range(N)]

for i in range(N):
    u = i / (N - 1)
    for j in range(N):
        v = j / (N - 1)
        # x
        tab[i][j][0] = (
            -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
        ) * math.cos(math.pi * v)
        # y
        tab[i][j][1] = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
        # z
        tab[i][j][2] = (
            -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
        ) * math.sin(math.pi * v)

        colors[i][j][0] = random()
        colors[i][j][1] = random()
        colors[i][j][2] = random()

for j in range(N):
    colors[0][j] = colors[0][N - 1]

for i in range(N):
    colors[i][0] = colors[N - 1][0]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)
    axes()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N - 1):
        for j in range(N - 1):
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])
            glColor3fv(colors[i + 1][j])
            glVertex3fv(tab[i + 1][j])
    glEnd()

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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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


if __name__ == "__main__":
    main()
