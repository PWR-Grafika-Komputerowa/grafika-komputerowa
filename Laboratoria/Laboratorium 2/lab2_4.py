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


def rysuj_prostokat(x, y, a, b, d=0.0):
    a = a * (1.0 + d)
    b = b * (1.0 + d)

    glBegin(GL_TRIANGLES)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y + b)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y + b)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y + b)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    random.seed(10)

    rysuj_prostokat(-80.0, -30.0, 50.0, 60.0)
    rysuj_prostokat(0.0, -30.0, 50.0, 60.0, 0.4)

    glFlush()


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
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
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
        glfwWaitEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()