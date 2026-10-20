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

def rectangle(x, y, a, b, i=0, r=0):

    if r == 0:
        glColor3f(0.5, 0.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y)
        glVertex2f(x + b, y)
        glVertex2f(x, y - a)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x + b, y - a)
        glVertex2f(x + b, y)
        glVertex2f(x, y - a)
        glEnd()

    elif r == 1:

        if i == 0:
            return

        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y)
        glVertex2f(x + b, y)
        glVertex2f(x, y - a)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x + b, y - a)
        glVertex2f(x + b, y)
        glVertex2f(x, y - a)
        glEnd()

        # PIERWSZA KOLUMNA
        i -= 1
        a_new = a / 3
        b_new = b / 3
        rectangle(x,y,a_new, b_new, i, 1)

        

        x_new = x
        y_new = 2 * y / 3
        rectangle(x_new,y_new,a_new, b_new, i, 1)

        # CAŁOŚĆ
        # TRÓJKĄT GÓRNY
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new, y_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new + b_new, y_new - a_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()


        x_new = x
        y_new = 1 * y / 3
        rectangle(x_new,y_new,a_new, b_new, i, 1)


        # DRUGA KOLUMNA
        x_new = 2 * x / 3
        y_new = y
        rectangle(x_new,y_new,a_new, b_new, i, 1)

        # CAŁOŚĆ
        # TRÓJKĄT GÓRNY
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new, y_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new + b_new, y_new - a_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()


        x_new = 2 * x / 3
        y_new = 2 * y / 3
        rectangle(x_new,y_new,a_new, b_new, i, 1)

        # CAŁOŚĆ
        # TRÓJKĄT GÓRNY
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new, y_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new + b_new, y_new - a_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        x_new = 2 * x / 3
        y_new = 1 * y / 3
        rectangle(x_new,y_new,a_new, b_new, i, 1)

        # CAŁOŚĆ
        # TRÓJKĄT GÓRNY
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new, y_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new + b_new, y_new - a_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()


        # TRZECIA KOLUMNA
        x_new = 1 * x / 3
        y_new = y
        rectangle(x_new,y_new,a_new, b_new, i, 1)

        # CAŁOŚĆ
        # TRÓJKĄT GÓRNY
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new, y_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new + b_new, y_new - a_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()


        x_new = 1 * x / 3
        y_new = 2 * y / 3
        rectangle(x_new,y_new,a_new, b_new, i, 1)

        # CAŁOŚĆ
        # TRÓJKĄT GÓRNY
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new, y_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new + b_new, y_new - a_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()


        x_new = 1 * x / 3
        y_new = 1 * y / 3
        rectangle(x_new,y_new,a_new, b_new, i, 1)

        # CAŁOŚĆ
        # TRÓJKĄT GÓRNY
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new, y_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()

        # TRÓJKĄT DOLNY
        glBegin(GL_TRIANGLES)
        glVertex2f(x_new + b_new, y_new - a_new)
        glVertex2f(x_new + b_new, y_new)
        glVertex2f(x_new, y_new - a_new)
        glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    x = -50
    y = 50
    a = 50
    b = 100
    i = 1
    r = 1

    glColor3f(0.5, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + b, y)
    glVertex2f(x, y - a)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(x + b, y - a)
    glVertex2f(x + b, y)
    glVertex2f(x, y - a)
    glEnd()

    rectangle(-50,50,50,100, 4, 1)

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
