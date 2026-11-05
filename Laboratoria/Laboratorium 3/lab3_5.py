#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

M = 5
N = 10

ctrl = [
    [
        [0.0, 0.0, 4.0],
        [1.0, 0.0, 4.0],
        [2.0, 0.0, 4.0],
        [3.0, 0.0, 4.0],
        [4.0, 1.0, 4.0],
    ],
    [
        [0.0, 0.0, 3.0],
        [1.0, 1.0, 3.0],
        [2.0, 1.0, 3.0],
        [3.0, 1.0, 3.0],
        [4.0, 1.0, 3.0],
    ],
    [
        [0.0, 1.0, 2.0],
        [1.0, 2.0, 2.0],
        [2.0, 6.0, 2.0],
        [3.0, 2.0, 2.0],
        [4.0, 1.0, 2.0],
    ],
    [
        [0.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [2.0, 1.0, 1.0],
        [3.0, 1.0, 1.0],
        [4.0, 1.0, 1.0],
    ],
    [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 0.0, 0.0],
        [4.0, 1.0, 0.0],
    ],
]


tab = [[[0.0] * 3 for i in range(N)] for j in range(N)]


def b(i, n, t):
    return math.comb(n, i) * t**i * (1.0 - t) ** (n - i)


for i in range(N):
    u = i / (N - 1)
    for j in range(N):
        v = j / (N - 1)
        for c in range(3):
            tab[i][j][c] = sum(
                ctrl[p][q][c] * b(p, M - 1, u) * b(q, M - 1, v)
                for p in range(M)
                for q in range(M)
            )


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def lines():
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)
    for p in range(M):
        for q in range(M):
            if p < M - 1:
                glVertex3fv(ctrl[p][q])
                glVertex3fv(ctrl[p + 1][q])
            if q < M - 1:
                glVertex3fv(ctrl[p][q])
                glVertex3fv(ctrl[p][q + 1])
    glEnd()


def surface():
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


def vertex(i, j):
    glColor3f(i / (N - 1), j / (N - 1), 1.0 - i / (N - 1))
    glVertex3fv(tab[i][j])


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(-2.0, -3.0, -2.0)
    glRotatef(20.0, 1.0, 0.0, 0.0)
    glRotatef(-30.0, 0.0, 1.0, 0.0)

    surface()
    lines()

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
