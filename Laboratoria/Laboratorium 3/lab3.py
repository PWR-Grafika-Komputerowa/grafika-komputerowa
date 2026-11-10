#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 30
punkty_jajka = []
kolory_jajka = []
punkty_torusa = []
kolory_torusa = []


def startup():
    global punkty_jajka, kolory_jajka, punkty_torusa, kolory_torusa
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    punkty_jajka = generuj_punkty_jajka(N)
    kolory_jajka = generuj_kolory_jajka(N)

    punkty_torusa = generuj_punkty_torusa(N)
    kolory_torusa = generuj_kolory_torusa(N)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def generuj_punkty_jajka(n):
    tab = [[[0.0] * 3 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        u = i / (n - 1)
        for j in range(n):
            v = j / (n - 1)

            r = (-90 * (u**5) + 225 * (u**4) - 270 * (u**3) + 180 * (u**2) - 45 * u)
            x = r * math.cos(math.pi * v)
            y = 160 * (u**4) - 320 * (u**3) + 160 * (u**2) - 5
            z = r * math.sin(math.pi * v)

            tab[i][j] = [x, y, z]
    return tab


def generuj_kolory_jajka(n):
    kolory = [[[random.random() for _ in range(3)] for _ in range(n)] for _ in range(n)]

    #wygladzenie na zapetleniu
    for i in range(n):
        kolory[n - 1 - i][n - 1] = kolory[i][0]

    c_dol = kolory[0][0]
    for j in range(n):
        kolory[0][j] = c_dol
        kolory[n - 1][j] = c_dol

    return kolory


#zadanie na 3.0
def rysuj_jajko_punkty(tab):
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for row in tab:
        for p in row:
            glVertex3f(p[0], p[1], p[2])
    glEnd()


#zadanie na 3.5
def rysuj_jajko_linie(tab):
    n = len(tab)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(n):
        for j in range(n):
            if i + 1 < n:
                glVertex3f(*tab[i][j])
                glVertex3f(*tab[i + 1][j])
            if j + 1 < n:
                glVertex3f(*tab[i][j])
                glVertex3f(*tab[i][j + 1])
    glEnd()


#zadanie na 4.0
def rysuj_jajko_trojkaty(tab, kolory):
    n = len(tab)
    glBegin(GL_TRIANGLES)
    for i in range(n - 1):
        for j in range(n - 1):
            #trojkat1: (i, j), (i + 1, j), (i, j + 1)
            glColor3f(*kolory[i][j])
            glVertex3f(*tab[i][j])

            glColor3f(*kolory[i + 1][j])
            glVertex3f(*tab[i + 1][j])

            glColor3f(*kolory[i][j + 1])
            glVertex3f(*tab[i][j + 1])

            #trojkat2: (i + 1, j), (i + 1, j + 1), (i, j + 1)
            glColor3f(*kolory[i + 1][j])
            glVertex3f(*tab[i + 1][j])

            glColor3f(*kolory[i + 1][j + 1])
            glVertex3f(*tab[i + 1][j + 1])

            glColor3f(*kolory[i][j + 1])
            glVertex3f(*tab[i][j + 1])
    glEnd()


#zadanie na 4.5
def rysuj_jajko_paski(tab, kolory):
    n = len(tab)
    for i in range(n - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(n):
            glColor3f(*kolory[i][j])
            glVertex3f(*tab[i][j])

            glColor3f(*kolory[i + 1][j])
            glVertex3f(*tab[i + 1][j])
        glEnd()


#zadanie na 5.0
def generuj_punkty_torusa(n, R=3.0, r=1.2):
    tab = [[[0.0] * 3 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        u = 2 * math.pi * i / (n - 1)
        for j in range(n):
            v = 2 * math.pi * j / (n - 1)

            x = (R + r * math.cos(v)) * math.cos(u)
            y = r * math.sin(v)
            z = (R + r * math.cos(v)) * math.sin(u)

            tab[i][j] = [x, y, z]
    return tab


def generuj_kolory_torusa(n):
    kolory = [[[random.random() for _ in range(3)] for _ in range(n)] for _ in range(n)]

    #wygladzenie koloru na zapetleniu
    for i in range(n):
        kolory[i][n - 1] = kolory[i][0]
    for j in range(n):
        kolory[n - 1][j] = kolory[0][j]

    return kolory


def rysuj_torus_paski(tab, kolory):
    n = len(tab)
    for i in range(n - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(n):
            glColor3f(*kolory[i][j])
            glVertex3f(*tab[i][j])

            glColor3f(*kolory[i + 1][j])
            glVertex3f(*tab[i + 1][j])
        glEnd()


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

    spin(time * 180 / 3.1415)

    #na 3.0
    rysuj_jajko_punkty(punkty_jajka)
    
    #na 3.5
    #rysuj_jajko_linie(punkty_jajka)
    
    #na 4.0
    #rysuj_jajko_trojkaty(punkty_jajka, kolory_jajka)
    
    #na 4.5
    #rysuj_jajko_paski(punkty_jajka, kolory_jajka)
    
    #na 5.0
    #rysuj_torus_paski(punkty_torusa, kolory_torusa)

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
