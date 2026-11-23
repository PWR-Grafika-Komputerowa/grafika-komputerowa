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

def draw_rectangle(x, y, a, b):
    hx = a / 2.0
    hy = b / 2.0

    #Wierzchołki
    bl = (x - hx, y - hy)  #bottom-left
    tl = (x - hx, y + hy)  #top-left
    tr = (x + hx, y + hy)  #top-right
    br = (x + hx, y - hy)  #bottom-right

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.2, 0.4)

    glVertex2f(bl[0], bl[1])
    glVertex2f(tl[0], tl[1])
    glVertex2f(tr[0], tr[1])

    #glColor3f(0.0, 1.0, 0.0)
    glVertex2f(bl[0], bl[1])
    glVertex2f(tr[0], tr[1])
    glVertex2f(br[0], br[1])

    glEnd()

def draw_sierpinski(x,y,a,b,d):
    if d==0:
        draw_rectangle(x,y,a,b)
        return
    new_a = a / 3.0
    new_b = b / 3.0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            # Obliczenie środka
            new_x = x + i * new_a
            new_y = y + j * new_b

            # Rekurencyjne wywołanie dla mniejszego prostokąta ze zmniejszoną głębokością
            draw_sierpinski(new_x, new_y, new_a, new_b, d - 1)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    depth_level = 4
    draw_sierpinski(0.0, 0.0, 160.0, 100.0, depth_level)

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
