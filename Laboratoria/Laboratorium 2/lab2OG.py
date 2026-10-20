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

def rectangle(x, y, a, b, r1, g1, b1, r2, g2, b2, d = 0.0):
    Ax = x - a/2 + d
    Ay = y - b/2
    Bx = x + a/2
    By = y - b/2
    Cx = x + a/2 - d
    Cy = y + b/2
    Dx = x - a/2 - d
    Dy = y + b/2 + d   

    glColor3f(r1, g1, b1)
    glBegin(GL_TRIANGLES)
    glVertex2f(Ax, Ay)
    glVertex2f(Bx, By)
    glVertex2f(Cx, Cy)
    glEnd()
    
    glColor3f(r2, g2, b2)
    glBegin(GL_TRIANGLES)
    glVertex2f(Ax, Ay)
    glVertex2f(Dx, Dy)
    glVertex2f(Cx, Cy)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 43.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-50.0, -43.3)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, -43.3)
    glEnd()

    glFlush()
    
    glClear(GL_COLOR_BUFFER_BIT)
    rectangle(0.0, 0.0, 50, 80, random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), 12.5)
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
    
    random.seed()
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
