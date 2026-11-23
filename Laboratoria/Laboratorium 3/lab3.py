#!/usr/bin/env python3
import sys
import numpy as np

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


POINTS_PER_AXIS = 35

egg_vertices = np.zeros((POINTS_PER_AXIS, POINTS_PER_AXIS, 3))

draw_egg = None


def compute_egg_vertices():
    global egg_colors
    u_values = np.linspace(0.0, 1.0, POINTS_PER_AXIS)
    v_values = np.linspace(0.0, 1.0, POINTS_PER_AXIS)

    u, v = np.meshgrid(u_values, v_values, indexing='ij')

    egg_vertices[:, :, 0] = (-90 * u**5 + 225 * u**4 - 270 * u**3           # x
                             + 180 * u**2 - 45 * u) * np.cos(np.pi * v)

    egg_vertices[:, :, 1] = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5        # y

    egg_vertices[:, :, 2] = (-90 * u**5 + 225 * u**4 - 270 * u**3           # z
                             + 180 * u**2 - 45 * u) * np.sin(np.pi * v)

    egg_colors = np.random.rand(POINTS_PER_AXIS, POINTS_PER_AXIS, 3)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    compute_egg_vertices()


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


def draw_egg_points():
    glColor3f(240 / 255.0, 234 / 255.0, 214 / 255.0)
    glBegin(GL_POINTS)
    for u in range(POINTS_PER_AXIS):
        for v in range(POINTS_PER_AXIS):
            glVertex3fv(egg_vertices[u][v])
    glEnd()

def connect_vertices():
    glColor3f(240 / 255.0, 234 / 255.0, 214 / 255.0)
    glBegin(GL_LINES)
    for u in range(POINTS_PER_AXIS):
        for v in range(POINTS_PER_AXIS):
            if u < POINTS_PER_AXIS - 1:
                glVertex3fv(egg_vertices[u][v])
                glVertex3fv(egg_vertices[u + 1][v])
            if v < POINTS_PER_AXIS - 1:
                glVertex3fv(egg_vertices[u][v])
                glVertex3fv(egg_vertices[u][v + 1])
    glEnd()


def connect_vertices_with_triangles():
    glShadeModel(GL_FLAT)
    glBegin(GL_TRIANGLES)

    for u in range(POINTS_PER_AXIS - 1):
        for v in range(POINTS_PER_AXIS - 1):
            glColor3fv(egg_colors[u][v])
            glVertex3fv(egg_vertices[u][v])

            glColor3fv(egg_colors[u + 1][v])
            glVertex3fv(egg_vertices[u + 1][v])

            glColor3fv(egg_colors[u][v + 1])
            glVertex3fv(egg_vertices[u][v + 1])

            glColor3fv(egg_colors[u + 1][v])
            glVertex3fv(egg_vertices[u + 1][v])

            glColor3fv(egg_colors[u + 1][v + 1])
            glVertex3fv(egg_vertices[u + 1][v + 1])

            glColor3fv(egg_colors[u][v + 1])
            glVertex3fv(egg_vertices[u][v + 1])
    glEnd()

def connect_vertices_with_strips():
    glShadeModel(GL_FLAT)
    for u in range(POINTS_PER_AXIS - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for v in range(POINTS_PER_AXIS):
            glColor3fv(egg_colors[u][v])
            glVertex3fv(egg_vertices[u][v])
 
            glColor3fv(egg_colors[u + 1][v])
            glVertex3fv(egg_vertices[u + 1][v])
        glEnd()


MODES = {
    "points": draw_egg_points,                      # Zadanie (1)
    "lines": connect_vertices,                      # Zadanie (2)
    "triangles": connect_vertices_with_triangles,   # Zadanie (3)
    "strips": connect_vertices_with_strips,         # Zadanie (4)
}


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    angle = time * (180 / np.pi)
    spin(angle)

    axes()
    draw_egg()

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
    global draw_egg

    if len(sys.argv) < 2:
        print("Missing argument. Run e.g.: python3 lab3.py points")
        print("Available options: 'points', 'lines', 'triangles', 'strips'.")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode not in MODES:
        print(f"Invalid argument '{sys.argv[1]}'. Run e.g.: python3 lab3.py points")
        print("Available options: 'points', 'lines', 'triangles', 'strips'.")
        sys.exit(1)
    draw_egg = MODES[mode]

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