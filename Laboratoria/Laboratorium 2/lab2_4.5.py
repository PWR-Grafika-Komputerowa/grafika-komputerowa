import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)


def shutdown():
    pass


def rysuj_prostokat(x, y, a, b, d=0.0):
    a = a * (1.0 + d)
    b = b * (1.0 + d)

    glColor3f(0.6, 0.2, 0.0)
    glBegin(GL_TRIANGLES)

    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)

    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)

    glEnd()


def dywan_sierpinskiego(x, y, a, b, stopien):
    if stopien == 0:
        rysuj_prostokat(x, y, a, b)
    else:
        nowe_a = a / 3.0
        nowe_b = b / 3.0

        for wiersz in range(3):
            for kolumna in range(3):
                if wiersz == 1 and kolumna == 1:
                    continue

                nowy_x = x + kolumna * nowe_a
                nowy_y = y + wiersz * nowe_b

                dywan_sierpinskiego(nowy_x, nowy_y, nowe_a, nowe_b, stopien - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    stopien_rekurencji = 3
    dywan_sierpinskiego(-80.0, -60.0, 160.0, 120.0, stopien_rekurencji)

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