#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 100

tab = [[[0] * 3 for i in range(N)] for j in range(N)]

u_tab = [i / (N - 1) for i in range(N)]
v_tab = [j / (N - 1) for j in range(N)]


def policz_jajko():
    for i in range(N):
        u = u_tab[i]

        fu = -90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u
        y  = 160*u**4 - 320*u**3 + 160*u**2 - 5

        for j in range(N):
            v = v_tab[j]

            # pelny obrot 
            x = fu * math.cos(2 * math.pi * v)
            z = fu * math.sin(2 * math.pi * v)

            tab[i][j][0] = x
            tab[i][j][1] = y
            tab[i][j][2] = z


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    policz_jajko()


def shutdown():
    pass


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


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()

    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3fv(tab[i][j])

    glEnd()

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
