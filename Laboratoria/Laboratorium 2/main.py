#!/usr/bin/env python3
import os
import sys
import random



from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

ZADANIE = 4


def zadanie_1():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, -50.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(50.0, -50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 50.0)
    glEnd()


def zadanie_2_3(x, y, a, b, d=0.0):
    a_def = a * (1.0 + d)
    b_def = b * (1.0 + d)

    c1 = (random.random(), random.random(), random.random())
    c2 = (random.random(), random.random(), random.random())

    glBegin(GL_TRIANGLES)
    glColor3f(*c1)
    glVertex2f(x, y)
    glVertex2f(x + a_def, y)
    glVertex2f(x, y + b_def)

    glColor3f(*c2)
    glVertex2f(x + a_def, y)
    glVertex2f(x + a_def, y + b_def)
    glVertex2f(x, y + b_def)
    glEnd()


def zadanie_4(x, y, a, b, stopien):
    if stopien == 0:
        zadanie_2_3(x, y, a, b, 0.0)
        return

    szer = a / 3.0
    wys = b / 3.0

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            zadanie_4(x + i * szer, y + j * wys, szer, wys, stopien - 1)


def zadanie_5(x_start, y_start, rozmiar, stopien):
    podzial = 3 ** stopien
    krok = rozmiar / podzial

    for i in range(podzial):
        for j in range(podzial):
            pusty = False
            temp_i, temp_j = i, j

            for k in range(stopien):
                if temp_i % 3 == 1 and temp_j % 3 == 1:
                    pusty = True
                    break
                temp_i //= 3
                temp_j //= 3

            if not pusty:
                zadanie_2_3(x_start + i * krok, y_start + j * krok, krok, krok, 0.0)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(12345)

    if ZADANIE == 1:
        zadanie_1()
    elif ZADANIE == 2:
        zadanie_2_3(-50.0, -50.0, 100.0, 60.0, 0.0)
    elif ZADANIE == 3:
        zadanie_2_3(-50.0, -50.0, 100.0, 60.0, 0.2)
    elif ZADANIE == 4:
        zadanie_4(-80.0, -80.0, 160.0, 160.0, 3)
    elif ZADANIE == 5:
        zadanie_5(-80.0, -80.0, 160.0, 3)

    glFlush()


def update_viewport(window, width, height):
    if width == 0: width = 1
    if height == 0: height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(600, 600, "Lab2", None, None)
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