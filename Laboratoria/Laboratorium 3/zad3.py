#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 20
SEED = 42

vertices = [[[0.0 for _ in range(3)] for _ in range(N)] for _ in range(N)]
colors = [[[0.0 for _ in range(3)] for _ in range(N)] for _ in range(N)]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    random.seed(SEED)
    generate_egg()


def shutdown():
    pass


def generate_egg():
    for i in range(N):
        for j in range(N):
            u = i / (N - 1)
            v = j / (N - 1)

            poly = -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u

            vertices[i][j][0] = poly * math.cos(math.pi * v)
            vertices[i][j][1] = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            vertices[i][j][2] = poly * math.sin(math.pi * v)

            colors[i][j] = [random.random(), random.random(), random.random()]


def draw_egg():
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3fv(vertices[i][j])
    glEnd()


def draw_egg_lines():
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)
    for i in range(N - 1):
        for j in range(N - 1):
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i + 1][j])

            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i][j + 1])
    glEnd()


def vertex(i, j):
    glColor3fv(colors[i][j])
    glVertex3fv(vertices[i][j])


def draw_egg_triangles():
    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            vertex(i, j)
            vertex(i + 1, j)
            vertex(i, j + 1)

            vertex(i, j + 1)
            vertex(i + 1, j)
            vertex(i + 1, j + 1)
    glEnd()


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

    axes()
    spin(time * 180 / math.pi)

    # draw_egg()
    # draw_egg_lines()
    draw_egg_triangles()

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


if __name__ == '__main__':
    main()