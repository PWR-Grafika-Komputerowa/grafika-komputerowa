import sys
import math
import random
import numpy as np

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 30


tab_egg = np.zeros((N, N, 3))
tab_torus = np.zeros((N, N, 3))
colors = np.zeros((N, N, 3))

current_model = 1


def key_callback(window, key, scancode, action, mods):
    global current_model
    if action == GLFW_PRESS:
        if key == GLFW_KEY_1:
            current_model = 1
        elif key == GLFW_KEY_2:
            current_model = 2


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def startup():
    global tab_egg, tab_torus, colors
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    R = 4.0
    r = 1.5

    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)

            # zadania na 3 do 4.5
            x_e = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
            y_e = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            z_e = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

            tab_egg[i][j][0] = x_e
            tab_egg[i][j][1] = y_e
            tab_egg[i][j][2] = z_e

            #ZADANIE 5 - dodatkowe wzory
            x_t = (R + r * math.cos(2 * math.pi * v)) * math.cos(2 * math.pi * u)
            y_t = (R + r * math.cos(2 * math.pi * v)) * math.sin(2 * math.pi * u)
            z_t = r * math.sin(2 * math.pi * v)

            tab_torus[i][j][0] = x_t
            tab_torus[i][j][1] = y_t
            tab_torus[i][j][2] = z_t

            # Kolory (wspólne dla obu modeli)
            colors[i][j][0] = random.random()
            colors[i][j][1] = random.random()
            colors[i][j][2] = random.random()


    for i in range(N):
        colors[i][N - 1] = colors[i][0]
    for j in range(N):
        colors[N - 1][j] = colors[0][j]


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


def render_model(tab):
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])

            glColor3fv(colors[i + 1][j])
            glVertex3fv(tab[i + 1][j])
        glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()
    angle = time * 180 / math.pi
    spin(angle)


    if current_model == 1:
        render_model(tab_egg)
    else:
        render_model(tab_torus)

    glFlush()


def update_viewport(window, width, height):
    if width == 0: width = 1
    if height == 0: height = 1
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

    window = glfwCreateWindow(400, 400, "Jajko i Torus", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    glfwSetKeyCallback(window, key_callback)

    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == '__main__':
    main()