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

def draw_rectangle(x, y, a, b):
    glColor3f(0.2, 0.6, 0.9)

    glBegin(GL_TRIANGLES)

    # Pierwszy trójkąt (lewy dolny -> prawy dolny -> prawy górny)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)

    # Drugi trójkąt (lewy dolny -> prawy górny -> lewy górny)
    glVertex2f(x, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)

    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    draw_rectangle(-50.0, -30.0, 100.0, 60.0)
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