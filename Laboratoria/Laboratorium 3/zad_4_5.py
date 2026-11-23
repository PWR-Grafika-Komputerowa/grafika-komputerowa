#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 25
vertices = []
colors = []


def generate_egg_vertices(n):
    tab = [[[0.0] * 3 for _ in range(n)] for _ in range(n)]
    u_values = [i / (n - 1) for i in range(n)]
    v_values = [j / (n - 1) for j in range(n)]

    for i, u in enumerate(u_values):
        poly_u = -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
        y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
        for j, v in enumerate(v_values):
            x = poly_u * math.cos(math.pi * v)
            z = poly_u * math.sin(math.pi * v)
            tab[i][j] = [x, y, z]

    return tab


def generate_egg_colors(n):
    tab = [
        [[random.random(), random.random(), random.random()] for _ in range(n)]
        for _ in range(n)
    ]

    # Spójność kolorów na szwie łączenia brzegów dziedziny (v = 0 oraz v = 1):
    # wierzchołek (u, 1) ma te same współrzędne 3D co (1 - u, 0)
    for i in range(n):
        tab[i][n - 1] = tab[n - 1 - i][0][:]

    # Spójność kolorów na biegunie dolnym (u = 0 oraz u = 1 -> (0, -5, 0))
    bottom_color = tab[0][0][:]
    for j in range(n):
        tab[0][j] = bottom_color[:]
        tab[n - 1][j] = bottom_color[:]

    # Spójność kolorów na biegunie górnym (u = 0.5 -> (0, 5, 0) dla nieparzystego N)
    if n % 2 == 1:
        mid = n // 2
        top_color = tab[mid][0][:]
        for j in range(n):
            tab[mid][j] = top_color[:]

    return tab


def startup():
    global vertices, colors
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_FLAT)
    vertices = generate_egg_vertices(N)
    colors = generate_egg_colors(N)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def draw_egg():
    # Każda warstwa modelu (pomiędzy i oraz i + 1) budowana jest jednym paskiem trójkątów
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3f(*colors[i][j])
            glVertex3f(*vertices[i][j])
            glColor3f(*colors[i + 1][j])
            glVertex3f(*vertices[i + 1][j])
        glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)
    draw_egg()

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
