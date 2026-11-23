#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 25
vertices = []


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


def startup():
    global vertices
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    vertices = generate_egg_vertices(N)


def shutdown():
    pass


def draw_egg():
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3f(*vertices[i][j])
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

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
