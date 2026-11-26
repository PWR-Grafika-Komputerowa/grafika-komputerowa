import sys
import math
import random
from glfw.GLFW import *
from OpenGL.GL import *

ZADANIE = 4.0  # Wpisz: 3.0, 3.5 albo 4.0
N = 31

punkty = []
kolory = []


def startup():
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glPointSize(3)

    for i in range(N):
        wiersz = []
        kolory_wiersza = []
        u = i / (N - 1)

        for j in range(N):
            v = j / (N - 1)
            r = -90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u
            x = r * math.cos(math.pi * v)
            y = 160*u**4 - 320*u**3 + 160*u**2 - 5
            z = r * math.sin(math.pi * v)
            wiersz.append((x, y, z))
            kolory_wiersza.append((random.random(), random.random(), random.random()))

        punkty.append(wiersz)
        kolory.append(kolory_wiersza)


def wierzcholek(i, j):
    glColor3fv(kolory[i][j])
    glVertex3fv(punkty[i][j])


def jajko():
    if ZADANIE == 3.0:
        glBegin(GL_POINTS)
        glColor3f(1, 1, 1)
        for i in range(N):
            for j in range(N):
                glVertex3fv(punkty[i][j])
        glEnd()

    elif ZADANIE == 3.5:
        glBegin(GL_LINES)
        glColor3f(1, 1, 1)
        for i in range(N):
            for j in range(N):
                if i < N - 1:
                    glVertex3fv(punkty[i][j])
                    glVertex3fv(punkty[i + 1][j])
                if j < N - 1:
                    glVertex3fv(punkty[i][j])
                    glVertex3fv(punkty[i][j + 1])
        glEnd()

    elif ZADANIE == 4.0:
        glBegin(GL_TRIANGLES)
        for i in range(N - 1):
            for j in range(N - 1):
                wierzcholek(i, j)
                wierzcholek(i + 1, j)
                wierzcholek(i, j + 1)

                wierzcholek(i, j + 1)
                wierzcholek(i + 1, j)
                wierzcholek(i + 1, j + 1)
        glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if ZADANIE >= 3.5:
        kat = time * 180 / math.pi
        glRotatef(kat, 1, 0, 0)
        glRotatef(kat, 0, 1, 0)
        glRotatef(kat, 0, 0, 1)

    jajko()
    glFlush()


def update_viewport(window, width, height):
    width = max(width, 1)
    height = max(height, 1)
    proporcje = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    if width <= height:
        glOrtho(-7.5, 7.5, -7.5/proporcje, 7.5/proporcje, 7.5, -7.5)
    else:
        glOrtho(-7.5*proporcje, 7.5*proporcje, -7.5, 7.5, 7.5, -7.5)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(1)

    window = glfwCreateWindow(600, 600, 'Lab 3', None, None)
    if not window:
        glfwTerminate()
        sys.exit(1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    startup()
    update_viewport(window, *glfwGetFramebufferSize(window))

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == '__main__':
    main()
