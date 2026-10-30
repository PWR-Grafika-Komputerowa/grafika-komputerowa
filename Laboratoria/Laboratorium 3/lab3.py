#!/usr/bin/env python3
import sys
import numpy as np
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 25
ZAD = 5

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

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

def compute_egg(n):
    # Tablica wierzchołków o rozmiarze N x N x 3
    tab = np.zeros((n, n, 3))

    # N-elementowe tablice wartości dla parametrów u i v z przedziału [0.0, 1.0]
    u_vals = np.linspace(0.0, 1.0, n)
    v_vals = np.linspace(0.0, 1.0, n)

    for i in range(n):
        u = u_vals[i]

        poly_xz = -90.0 * (u ** 5) + 225.0 * (u ** 4) - 270.0 * (u ** 3) + 180.0 * (u ** 2) - 45.0 * u

        y = 160.0 * (u ** 4) - 320.0 * (u ** 3) + 160.0 * (u ** 2) - 5.0

        for j in range(n):
            v = v_vals[j]
            x = poly_xz * math.cos(math.pi * v)
            z = poly_xz * math.sin(math.pi * v)

            tab[i][j][0] = x
            tab[i][j][1] = y
            tab[i][j][2] = z

    return tab


def compute_colors(n):

    colors = np.random.rand(n, n, 3)

    for i in range(n):
        colors[i][n - 1] = colors[n - 1 - i][0]
    return colors

jajko = compute_egg(N)
kolory = compute_colors(N)

SIERPINSKI_DEPTH = 3
def draw_pyramid(x, y, z, size):
    half = size / 2.0
    # Wierzchołek górny (szczyt ostrosłupa)
    top = (x, y + size, z)
    # 4 wierzchołki kwadratowej podstawy
    b_fl = (x - half, y, z + half)  # przedni-lewy
    b_fr = (x + half, y, z + half)  # przedni-prawy
    b_br = (x + half, y, z - half)  # tylny-prawy
    b_bl = (x - half, y, z - half)  # tylny-lewy
    glBegin(GL_TRIANGLES)
    # Ściana przednia
    glColor3f(1.0, 0.2, 0.2)
    glVertex3fv(top)
    glColor3f(0.8, 0.0, 0.0)
    glVertex3fv(b_fl)
    glVertex3fv(b_fr)
    # Ściana prawa
    glColor3f(0.2, 1.0, 0.2)
    glVertex3fv(top)
    glColor3f(0.0, 0.8, 0.0)
    glVertex3fv(b_fr)
    glVertex3fv(b_br)
    # Ściana tylna
    glColor3f(0.2, 0.4, 1.0)
    glVertex3fv(top)
    glColor3f(0.0, 0.2, 0.8)
    glVertex3fv(b_br)
    glVertex3fv(b_bl)
    # Ściana lewa
    glColor3f(1.0, 1.0, 0.2)
    glVertex3fv(top)
    glColor3f(0.8, 0.8, 0.0)
    glVertex3fv(b_bl)
    glVertex3fv(b_fl)
    # Podstawa
    glColor3f(0.7, 0.2, 0.8)
    glVertex3fv(b_fl)
    glVertex3fv(b_fr)
    glVertex3fv(b_br)
    glVertex3fv(b_fl)
    glVertex3fv(b_br)
    glVertex3fv(b_bl)
    glEnd()

def sierpinski_3d(x, y, z, size, depth):
    if depth == 0:
        draw_pyramid(x, y, z, size)
    else:
        half = size / 2.0
        q = size / 4.0
        # 1. Górny mniejszy ostrosłup
        sierpinski_3d(x, y + half, z, half, depth - 1)
        # 2-5. Cztery dolne mniejsze ostrosłupy w narożnikach podstawy
        sierpinski_3d(x - q, y, z + q, half, depth - 1)
        sierpinski_3d(x + q, y, z + q, half, depth - 1)
        sierpinski_3d(x + q, y, z - q, half, depth - 1)
        sierpinski_3d(x - q, y, z - q, half, depth - 1)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)
    axes()

    if ZAD == 1:
        # Rysowanie modelu jajka za pomocą punktów (GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        for i in range(N):
            for j in range(N):
                glVertex3fv(jajko[i][j])
        glEnd()
    if ZAD == 2:
        # Rysowanie modelu jajka za pomocą lini (GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for i in range(N-1):
            for j in range(N-1):
                glVertex3fv(jajko[i][j])
                glVertex3fv(jajko[i+1][j])

                glVertex3fv(jajko[i][j])
                glVertex3fv(jajko[i][j+1])
        glEnd()
    if ZAD == 3:
        # Rysowanie modelu jajka za pomocą trójkątów (GL_TRIANGLES)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        for i in range(N-1):
            for j in range(N-1):
                glColor3fv(kolory[i][j])
                glVertex3fv(jajko[i][j])

                glColor3fv(kolory[i+1][j])
                glVertex3fv(jajko[i+1][j])

                glColor3fv(kolory[i][j+1])
                glVertex3fv(jajko[i][j+1])


                glColor3fv(kolory[i+1][j])
                glVertex3fv(jajko[i+1][j])

                glColor3fv(kolory[i+1][j+1])
                glVertex3fv(jajko[i+1][j+1])

                glColor3fv(kolory[i][j+1])
                glVertex3fv(jajko[i][j+1])
        glEnd()
    if ZAD == 4:
        # Rysowanie modelu jajka za pomocą trójkątów (GL_TRIANGLE_STRIP)
        glColor3f(1.0, 1.0, 1.0)
        for i in range(N-1):
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(N):
                glColor3fv(kolory[i][j])
                glVertex3fv(jajko[i][j])

                glColor3fv(kolory[i+1][j])
                glVertex3fv(jajko[i+1][j])
            glEnd()
    if ZAD == 5:
        # Trójkąt Sierpińskiego 3D
        sierpinski_3d(0.0, -4.0, 0.0, 8.0, SIERPINSKI_DEPTH)
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
