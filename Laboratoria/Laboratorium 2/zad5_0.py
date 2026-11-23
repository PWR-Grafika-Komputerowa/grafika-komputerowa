#!/usr/bin/env python3
import sys
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def draw_triangle(a, b, c):
    glBegin(GL_TRIANGLES)
    glVertex2f(a[0], a[1])
    glVertex2f(b[0], b[1])
    glVertex2f(c[0], c[1])
    glEnd()

#Wyznacza punkt środkowy odcinka pomiędzy p1 a p2
def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)

def draw_sierpinski_triangle(a, b, c, depth):
    if depth == 0:
        draw_triangle(a, b, c)
        return

    ab_mid = midpoint(a, b)
    bc_mid = midpoint(b, c)
    ca_mid = midpoint(c, a)

    # Rekurencyjne wywołanie dla 3 narożnych trójkątów
    draw_sierpinski_triangle(a, ab_mid, ca_mid, depth - 1)
    draw_sierpinski_triangle(ab_mid, b, bc_mid, depth - 1)
    draw_sierpinski_triangle(ca_mid, bc_mid, c, depth - 1)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    top = (0.0, 80.0)
    left = (-80.0, -60.0)
    right = (80.0, -60.0)

    depth_level = 5
    draw_sierpinski_triangle(top, left, right, depth_level)

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
