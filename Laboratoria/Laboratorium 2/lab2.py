#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    # render_triangle()
    # render_rectangle(-50, 25,100,50)
    # render_distorted_rectangle(-50, 25, 100, 50, 2, 50)
    # render_serpinski_fractal(-50, 25, 100, 50, 6)
    glFlush()


# Funkcja do zadania 1 (rysowanie trójkąta)
def render_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, -50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, -50.0)
    glEnd()


# Funkcja do zadania 2 (rysowanie prostokąta)
def render_rectangle(x, y, width, height):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y)
    glVertex2f(x, y - height)
    glVertex2f(x + width, y - height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y - height)
    glEnd()


# Funkcja do zadania 3 (rysowanie kolorowego prosotkąta)
def render_distorted_rectangle(x, y, width, height, deformation=0.0, random_color=0.0):
    # deformowanie
    width = width * (1.0 * deformation)
    height = height * (1.0 * deformation)

    # kolorki
    random.seed(random_color)
    colors_1 = (random.random(), random.random(), random.random())
    colors_2 = (random.random(), random.random(), random.random())
    colors_3 = (random.random(), random.random(), random.random())
    colors_4 = (random.random(), random.random(), random.random())

    glBegin(GL_TRIANGLES)
    glColor3f(colors_1[0], colors_1[1], colors_1[2])
    glVertex2f(x, y)
    glColor3f(colors_2[0], colors_2[1], colors_2[2])
    glVertex2f(x, y - height)
    glColor3f(colors_3[0], colors_3[1], colors_3[2])
    glVertex2f(x + width, y - height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(colors_1[0], colors_1[1], colors_1[2])
    glVertex2f(x, y)
    glColor3f(colors_4[0], colors_4[1], colors_4[2])
    glVertex2f(x + width, y)
    glColor3f(colors_3[0], colors_3[1], colors_3[2])
    glVertex2f(x + width, y - height)
    glEnd()


# Funkcje do zadania 4 (rysowanie fraktala Sierpinskeigo)
def render_serpinski_fractal(x, y, width, height, ssimilarity):

    if ssimilarity == 0: return

    color_white = (1.0, 1.0, 1.0)
    color_red = (1.0, 0.0, 0.0)

    new_width = width / 3
    new_height = height / 3

    for i in range(3):
        for j in range(3):
            nx = x + (i * new_width)
            ny = y - (j * new_height)

            if i == 1 and j == 1:
                render_colored_rectangle(nx, ny, new_width, new_height, color_white)
            else:
                render_colored_rectangle(nx, ny, new_width, new_height, color_red)
                render_serpinski_fractal(nx, ny, new_width, new_height, ssimilarity - 1)

def render_colored_rectangle(x, y, width, height, color):
    glBegin(GL_TRIANGLES)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x, y)
    glVertex2f(x, y - height)
    glVertex2f(x + width, y - height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y - height)
    glEnd()


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
