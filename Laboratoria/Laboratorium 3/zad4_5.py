#!/usr/bin/env python3
import math
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Liczba próbek (gęstość siatki punktów)
N = 40

# Deklaracja tablicy wierzchołków o wymiarach N x N x 3
tab = [[[0.0] * 3 for _ in range(N)] for _ in range(N)]
colors = [[[0.0] * 3 for _ in range(N)] for _ in range(N)]

def calculate_egg_vertices():
    for i in range(N):
        # Parametr u z przedziału [0.0, 1.0]
        u = i / (N - 1)
        for j in range(N):
            # Parametr v z przedziału [0.0, 1.0]
            v = j / (N - 1)

            # Wspólny czynnik wielomianowy dla x oraz z
            w = (-90 * (u ** 5) + 225 * (u ** 4) - 270 * (u ** 3) + 180 * (u ** 2) - 45 * u)

            x = w * math.cos(math.pi * v)
            y = 160 * (u ** 4) - 320 * (u ** 3) + 160 * (u ** 2) - 5
            z = w * math.sin(math.pi * v)

            tab[i][j] = [x, y, z]
            colors[i][j] = [random.random(), random.random(), random.random()]

    # Nadpisanie kolorów na brzegach dziedziny (u, v), aby wyeliminować artefakty łączenia
    for i in range(N):
        # Wierzchołki dla v = 1 (j = N - 1) pokrywają się przestrzennie z v = 0 (j = 0) dla (N - 1 - i)
        colors[i][N - 1] = colors[N - 1 - i][0]

    # Ujednolicenie kolorów na biegunach (u = 0 i u = 1), gdzie punkty zbiegają się w (0, -5, 0)
    for j in range(N):
        colors[0][j] = colors[0][0]
        colors[N - 1][j] = colors[0][0]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    calculate_egg_vertices()


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

def draw_egg_triangle_strip():
    # Każda warstwa (pas między wierszem i oraz i + 1) rysowana jest jednym paskiem trójkątów
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])

            glColor3fv(colors[i + 1][j])
            glVertex3fv(tab[i + 1][j])
        glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()
    spin(time * 180.0 / math.pi)
    draw_egg_triangle_strip()

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
