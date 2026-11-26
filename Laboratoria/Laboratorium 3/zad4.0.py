import sys
import math
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 41


def startup():
    global punkty, kolory
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    punkty = przygotuj_jajko()
    kolory = przygotuj_kolory()
    glShadeModel(GL_SMOOTH)


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


def przygotuj_jajko():
    punkty = [[[0.0] * 3 for _ in range(N)] for _ in range(N)]
    u_values = [i / (N - 1) for i in range(N)]
    v_values = [j / (N - 1) for j in range(N)]
    for i in range(N):
        u = u_values[i]
        for j in range(N):
            v = v_values[j]
            r = -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
            x = r * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = r * math.sin(math.pi * v)
            punkty[i][j] = [x, y, z]
    return punkty


def przygotuj_kolory():
    random.seed(7)  # kolory powstaja tylko raz, a nie w kazdej klatce.
    return [[[random.random() for _ in range(3)] for _ in range(N)] for _ in range(N)]


def spin(kat):
    glRotatef(kat, 1, 0, 0)
    glRotatef(kat, 0, 1, 0)
    glRotatef(kat, 0, 0, 1)


def wierzcholek(punkty, kolory, i, j):
    glColor3fv(kolory[i][j])
    glVertex3fv(punkty[i][j])


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    axes()
    spin(time * 180 / math.pi)

    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            # Pierwsza polowa kratki.
            wierzcholek(punkty, kolory, i, j)
            wierzcholek(punkty, kolory, i + 1, j)
            wierzcholek(punkty, kolory, i, j + 1)
            # Druga polowa kratki.
            wierzcholek(punkty, kolory, i + 1, j)
            wierzcholek(punkty, kolory, i + 1, j + 1)
            wierzcholek(punkty, kolory, i, j + 1)
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


if __name__ == '__main__':
    main()
