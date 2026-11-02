#!/usr/bin/env python3
import random
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_rectangle(x, y, a, b, d=0.0, is_center=False):
    # Zapewnia stały kształt między klatkami (zapobiega migotaniu przy ciągłym renderowaniu)
    random.seed(42)

    # 1. Wyznaczenie bazowych punktów przed deformacją
    if is_center:
        x_min, x_max = x - a / 2.0, x + a / 2.0
        y_min, y_max = y - b / 2.0, y + b / 2.0
    else:
        x_min, x_max = x, x + a
        y_min, y_max = y, y + b

    # 2. Deformacja – dodanie losowego przesunięcia z zakresu [-d, d] do każdego z 4 wierzchołków
    v1 = (x_min + random.uniform(-d, d), y_min + random.uniform(-d, d))  # Lewy dolny
    v2 = (x_max + random.uniform(-d, d), y_min + random.uniform(-d, d))  # Prawy dolny
    v3 = (x_max + random.uniform(-d, d), y_max + random.uniform(-d, d))  # Prawy górny
    v4 = (x_min + random.uniform(-d, d), y_max + random.uniform(-d, d))  # Lewy górny

    glBegin(GL_TRIANGLES)

    # Pierwszy trójkąt (V1 -> V2 -> V3)
    glColor3f(0.8, 0.2, 0.2)  # Odcień czerwieni
    glVertex2f(*v1)
    glVertex2f(*v2)
    glVertex2f(*v3)

    # Drugi trójkąt (V1 -> V3 -> V4)
    glColor3f(0.2, 0.2, 0.8)  # Odcień niebieskiego
    glVertex2f(*v1)
    glVertex2f(*v3)
    glVertex2f(*v4)

    glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    #Prostokąt bez deformacji
    draw_rectangle(-80.0, -80.0, 40.0, 30.0, d=0.0, is_center=False)

    #Zdeformowany prostokąt
    draw_rectangle(0.0, 0.0, 80.0, 50.0, d=12.0, is_center=True)

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