#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


N = 20
array = [[[0.0] * 3 for j in range(N)] for i in range(N)]


def generate_egg():
    for i in range(N):
        u = 0.5 * i / (N - 1)

        f = (-90 * u**5 + 225 * u**4
             - 270 * u**3 + 180 * u**2 - 45 * u)

        y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5

        for j in range(N):
            v = j / N
            angle = 2 * math.pi * v

            x = f * math.cos(angle)
            z = f * math.sin(angle)

            array[i][j] = [x, y, z]



def draw_egg():
    glShadeModel(GL_SMOOTH)

    glBegin(GL_TRIANGLES)

    for i in range(N - 1):
        for j in range(N):
            next_j = (j + 1) % N

            # Pierwszy trojkat
            glColor3f(1.0, 0.0, 0.0)
            glVertex3fv(array[i][j])

            glColor3f(0.0, 1.0, 0.0)
            glVertex3fv(array[i + 1][j])

            glColor3f(0.0, 0.0, 1.0)
            glVertex3fv(array[i + 1][next_j])

            # Drugi trojkat
            glColor3f(1.0, 0.0, 0.0)
            glVertex3fv(array[i][j])

            glColor3f(0.0, 0.0, 1.0)
            glVertex3fv(array[i + 1][next_j])

            glColor3f(0.0, 1.0, 0.0)
            glVertex3fv(array[i][next_j])

    glEnd()




def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    generate_egg()


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

    # Rysowanie osi współrzędnych
    axes()

    # Zachowanie aktualnej macierzy
    glPushMatrix()

    # Obrót jajka wokół osi X o 25 stopni
    glRotatef(25.0, 1.0, 0.0, 0.0)

    # Obrót jajka wokół osi Y o 35 stopni
    glRotatef(35.0, 0.0, 1.0, 0.0)

    # Rysowanie jajka
    draw_egg()

    # Przywrócenie poprzedniej macierzy
    glPopMatrix()

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
