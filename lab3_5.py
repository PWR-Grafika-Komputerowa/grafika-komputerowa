#!/usr/bin/env python3
import sys
import math
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 30
jajko_wierzcholki = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]
jajko_kolory = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]

torus_wierzcholki = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]
torus_kolory = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]


def oblicz_modele():
    random.seed(42)
    R = 5.2
    r = 0.7

    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)

            x_j = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y_j = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5.0
            z_j = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)

            jajko_wierzcholki[i][j] = [x_j, y_j, z_j]
            jajko_kolory[i][j] = [random.random(), random.random(), random.random()]

            x_t = (R + r * math.cos(2.0 * math.pi * v)) * math.cos(2.0 * math.pi * u)
            y_t = r * math.sin(2.0 * math.pi * v)
            z_t = (R + r * math.cos(2.0 * math.pi * v)) * math.sin(2.0 * math.pi * u)

            torus_wierzcholki[i][j] = [x_t, y_t, z_t]
            torus_kolory[i][j] = [random.random(), random.random(), random.random()]

    for i in range(N):
        jajko_kolory[i][N - 1] = [
            jajko_kolory[N - 1 - i][0][0],
            jajko_kolory[N - 1 - i][0][1],
            jajko_kolory[N - 1 - i][0][2]
        ]
        torus_kolory[i][N - 1] = torus_kolory[i][0]

    for j in range(N):
        torus_kolory[N - 1][j] = torus_kolory[0][j]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    oblicz_modele()


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


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def rysuj_siatke_paskowa(wierzcholki, kolory):
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3fv(kolory[i][j])
            glVertex3fv(wierzcholki[i][j])

            glColor3fv(kolory[i + 1][j])
            glVertex3fv(wierzcholki[i + 1][j])
        glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180.0 / math.pi)
    axes()
    rysuj_siatke_paskowa(jajko_wierzcholki, jajko_kolory)
    rysuj_siatke_paskowa(torus_wierzcholki, torus_kolory)

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