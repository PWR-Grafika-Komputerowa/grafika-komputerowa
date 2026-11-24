#!/usr/bin/env python3
import sys
import math
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 30
tab = np.zeros((N, N, 3))
colors = np.zeros((N, N, 3))


def generate_egg():
    global tab, colors
    np.random.seed(42)
    colors = np.random.rand(N, N, 3)

    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)

            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(2 * math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(2 * math.pi * v)

            tab[i][j][0] = x
            tab[i][j][1] = y
            tab[i][j][2] = z

    for i in range(N):
        colors[i][N - 1] = colors[N - 1 - i][0]


def spin(angle):
    glRotatef(angle, 1.0, 1.0, 0.0)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    generate_egg()


def shutdown():
    pass


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
    glShadeModel(GL_FLAT)

    axes()

    angle = time * 180.0 / math.pi
    spin(angle)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
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

    window = glfwCreateWindow(400, 400, "Zadanie 4 - Triangle Strip", None, None)
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