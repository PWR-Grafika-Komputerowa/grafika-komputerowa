#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glShadeModel(GL_SMOOTH)


def shutdown():
    pass

def rysowanie_prostokata(x,y,a,b, d=0.0):
    a=a*(1.0 + d * (2.0 * random.random() - 1.0))
    b=b*(1.0 + d * (2.0 * random.random() - 1.0))
    hx = a / 2.0
    hy = b / 2.0
    bl = (x-hx, y-hy)
    tl = (x-hx, y + hy)
    tr= (x+hx, y+hy)
    br= (x+hx, y-hy)

    #na 4.0 losowe kolory:
    c_bl = (random.random(), random.random(), random.random())
    c_tl = (random.random(), random.random(), random.random())
    c_tr = (random.random(), random.random(), random.random())
    c_br = (random.random(), random.random(), random.random())

    glBegin(GL_TRIANGLES)
    glColor3f(*c_bl)
    glVertex2f(*bl)
    glColor3f(*c_br)
    glVertex2f(*br)
    glColor3f(*c_tr)
    glVertex2f(*tr)

    glColor3f(*c_bl)
    glVertex2f(*bl)
    glColor3f(*c_tr)
    glVertex2f(*tr)
    glColor3f(*c_tl)
    glVertex2f(*tl)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES) #kazdy wierzcholej ma inny kolor:
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-80.0, -20.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-20.0, -20.0)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(-50.0, -80.0)
    glEnd()

    # losowe kolory i max 25% deformacji, seed dobry dodatek aby nie migotaly kolory
    random.seed(7)
    rysowanie_prostokata(50.0, -35.0, 60.0, 50.0, 0.25)
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
