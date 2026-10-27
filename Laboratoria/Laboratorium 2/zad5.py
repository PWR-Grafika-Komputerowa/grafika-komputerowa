#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

RANDOM_SEED = random.randint(0, 1000000)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_triangle(x, y, a, h):
    
    glColor3f(random.random(), random.random(), random.random())

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)                  # Lewy dolny wierzchołek
    glVertex2f(x + a, y)              # Prawy dolny wierzchołek
    glVertex2f(x + a / 2.0, y + h)    # Górny (środkowy) wierzchołek
    glEnd()


def draw_sierpinski_triangle(x, y, a, h, level):
    if level == 0:
        draw_triangle(x, y, a, h)
    else:
        new_a = a / 2.0
        new_h = h / 2.0

        draw_sierpinski_triangle(x, y, new_a, new_h, level - 1)

        draw_sierpinski_triangle(x + new_a, y, new_a, new_h, level - 1)

        draw_sierpinski_triangle(x + new_a / 2.0, y + new_h, new_a, new_h, level - 1)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(RANDOM_SEED)
    
    draw_sierpinski_triangle(-80.0, -70.0, 160.0, 140.0, level=4)

    glFlush()

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
        glfwWaitEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()