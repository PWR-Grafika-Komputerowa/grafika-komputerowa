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

def draw_rectangle(x, y, a, b, d=0.0):
    # d=40.0
    a_deformed = a + d;
    b_deformed = b + d;
    hx = a_deformed / 2.0
    hy = b_deformed / 2.0

    #Wierzchołki
    bl = (x - hx, y - hy)  #bottom-left
    tl = (x - hx, y + hy)  #top-left
    tr = (x + hx, y + hy)  #top-right
    br = (x + hx, y - hy)  #bottom-right

    random_r = random.random()
    random_g = random.random()
    random_b = random.random()
    glBegin(GL_TRIANGLES)
    glColor3f(random_r, random_g, random_b)

    glVertex2f(bl[0], bl[1])
    glVertex2f(tl[0], tl[1])
    glVertex2f(tr[0], tr[1])

    #glColor3f(0.0, 1.0, 0.0)
    glVertex2f(bl[0], bl[1])
    glVertex2f(tr[0], tr[1])
    glVertex2f(br[0], br[1])

    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    random.seed(67)
    draw_rectangle(0.0, 0.0, 100.0, 60.0)

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
