#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


ZADANIE = 4.0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


# Pomocnicza funkcja do rysowania prostokąta (wykorzystywana w zadaniach 3.5, 4.0 oraz 4.5)
def draw_rectangle(x, y, a, b, d=0.0, random_color=False):
    dx1 = (random.random() - 0.5) * d * a
    dy1 = (random.random() - 0.5) * d * b
    dx2 = (random.random() - 0.5) * d * a
    dy2 = (random.random() - 0.5) * d * b
    dx3 = (random.random() - 0.5) * d * a
    dy3 = (random.random() - 0.5) * d * b
    dx4 = (random.random() - 0.5) * d * a
    dy4 = (random.random() - 0.5) * d * b

    x1, y1 = x, y
    x2, y2 = x + a, y
    x3, y3 = x + a, y + b
    x4, y4 = x, y + b

    if random_color:
        r1, g1, b1 = random.random(), random.random(), random.random()
        r2, g2, b2 = random.random(), random.random(), random.random()
        r3, g3, b3 = random.random(), random.random(), random.random()
        r4, g4, b4 = random.random(), random.random(), random.random()
    else:
        r1, g1, b1 = 0.7, 0.3, 0.15
        r2, g2, b2 = 0.7, 0.3, 0.15
        r3, g3, b3 = 0.7, 0.3, 0.15
        r4, g4, b4 = 0.7, 0.3, 0.15

    glBegin(GL_TRIANGLES)
    glColor3f(r1, g1, b1)
    glVertex2f(x1 + dx1, y1 + dy1)
    glColor3f(r2, g2, b2)
    glVertex2f(x2 + dx2, y2 + dy2)
    glColor3f(r3, g3, b3)
    glVertex2f(x3 + dx3, y3 + dy3)

    glColor3f(r1, g1, b1)
    glVertex2f(x1 + dx1, y1 + dy1)
    glColor3f(r3, g3, b3)
    glVertex2f(x3 + dx3, y3 + dy3)
    glColor3f(r4, g4, b4)
    glVertex2f(x4 + dx4, y4 + dy4)
    glEnd()



#  FUNKCJA DLA ZADANIA 3.0

def render_3_0(time):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, -50.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(50.0, -50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 50.0)
    glEnd()



#  FUNKCJA DLA ZADANIA 3.5

def render_3_5(time):
    draw_rectangle(-40.0, -30.0, 80.0, 60.0, d=0.0, random_color=False)



#  FUNKCJA DLA ZADANIA 4.0
def render_4_0(time):
    random.seed(123)
    draw_rectangle(-50.0, -40.0, 100.0, 80.0, d=1.15, random_color=True)



#  FUNKCJA DLA ZADANIA 4.5

def draw_sierpinski_carpet(x, y, a, b, depth):
    if depth == 0:
        draw_rectangle(x, y, a, b, d=0.0, random_color=False)
    else:
        w3 = a / 3.0
        h3 = b / 3.0
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                draw_sierpinski_carpet(x + i * w3, y + j * h3, w3, h3, depth - 1)

def render_4_5(time):
    draw_sierpinski_carpet(-80.0, -80.0, 160.0, 160.0, depth=3)


# Główna funkcja renderująca wybierająca odpowiednią metodę
def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    if ZADANIE == 3.0:
        render_3_0(time)
    elif ZADANIE == 3.5:
        render_3_5(time)
    elif ZADANIE == 4.0:
        render_4_0(time)
    elif ZADANIE == 4.5:
        render_4_5(time)

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
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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
