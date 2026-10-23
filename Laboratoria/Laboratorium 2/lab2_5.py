import sys
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)


def shutdown():
    pass


def rysuj_trojkat(x, y, a, b):
    glColor3f(random.random(), random.random(), random.random())
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a / 2.0, y + b)
    glEnd()


def trojkat_sierpinskiego(x, y, a, b, stopien):
    if stopien == 0:
        rysuj_trojkat(x, y, a, b)
    else:
        pol_a = a / 2.0
        pol_b = b / 2.0

        trojkat_sierpinskiego(x, y, pol_a, pol_b, stopien - 1)
        trojkat_sierpinskiego(x + pol_a, y, pol_a, pol_b, stopien - 1)
        trojkat_sierpinskiego(x + pol_a / 2.0, y + pol_b, pol_a, pol_b, stopien - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(25)

    trojkat_sierpinskiego(-80.0, -70.0, 160.0, 140.0, 5)

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