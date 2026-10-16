#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0) # ustawia kolor czyszczenia ekranu (kolor tła)


def shutdown():
    pass

def draw_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 0.0)

    glColor3f(0.5, 0.0, 0.2)
    glVertex2f(0.0, 65.0)

    glColor3f(0.5, 0.5, 0.5)
    glVertex2f(65.0, 0.0)
    glEnd()

def draw_rectangle(x, y, a, b, d=0.0):
    def randomizer():
        return random.uniform(-d, d) if d > 0.0 else 0.0

    v1 = (x + randomizer(), y + randomizer())
    v2 = (x + a + randomizer(), y + randomizer())
    v3 = (x + a + randomizer(), y + b + randomizer())
    v4 = (x + randomizer(), y + b + randomizer())

    v1_c = (random.random(), random.random(), random.random())
    v2_c = (random.random(), random.random(), random.random())
    v3_c = (random.random(), random.random(), random.random())
    v4_c = (random.random(), random.random(), random.random())

    glBegin(GL_TRIANGLES)
    glColor3f(*v1_c) # gwiazdka oznacza tutaj rozpakowanie argumentów
    glVertex2f(*v1)

    glColor3f(*v2_c)
    glVertex2f(*v2)

    glColor3f(*v3_c)
    glVertex2f(*v3)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(*v1_c)
    glVertex2f(*v1)

    glColor3f(*v3_c)
    glVertex2f(*v3)

    glColor3f(*v4_c)
    glVertex2f(*v4)
    glEnd()

def draw_sierpinski_carpet(x, y, a, b, depth, d=0.0):
    if depth == 0:
        draw_rectangle(x, y, a, b, d)
        return

    new_a = a / 3
    new_b = b / 3

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            sub_x = x + new_a * i
            sub_y = y + new_b * j

            draw_sierpinski_carpet(sub_x, sub_y, new_a, new_b, depth - 1, d)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT) # wypełnia obszar poprzedniej klatki kolorem tła

    random.seed(12345)

    draw_sierpinski_carpet(-75.0, -75.0, 150.0, 150.0, 3)

    # przekazuje zebrane polecenia do wykonania procesorowi graficznemu
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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0) # określa projekcję 2D
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Laboratorium 2", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1) # płynna zmiana klatek z częstotliwością odświeżania monitora

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window) # wyświetlenie gotowego kadru na ekranie
        glfwPollEvents() # obsługa kliknięć myszą i przycisków
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
