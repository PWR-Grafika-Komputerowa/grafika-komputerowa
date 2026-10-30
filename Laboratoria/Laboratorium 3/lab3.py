#!/usr/bin/env python3
import sys
import random
from math import cos, sin, pi

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

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
    spin(time * 180 / 3.1415)
    axes()
    generate_jajo_wireframe(N)
    #generate_jajo_triangles(N)
    #generate_jajo_trianglestrip(N)
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

def generate_jajo_wireframe(N):
    global jajo

    if N < 2:
        return

    glColor3f(1.0, 1.0, 1.0)

    for i in range(N):
        glBegin(GL_LINE_STRIP)
        for j in range(N):
            glVertex3fv(jajo[i][j])
        glEnd()

    for j in range(N):
        glBegin(GL_LINE_STRIP)
        for i in range(N):
            glVertex3fv(jajo[i][j])
        glEnd()

def _random_triangle_color(p1, p2, p3):
    seed = 2166136261
    for vertex in (p1, p2, p3):
        for coordinate in vertex:
            seed ^= int(round(coordinate * 1_000_000)) & 0xFFFFFFFF
            seed = (seed * 16777619) & 0xFFFFFFFF

    rng = random.Random(seed)
    return rng.random(), rng.random(), rng.random()


def generate_jajo_triangles(N):
    if N < 2:
        return

    glShadeModel(GL_FLAT)
    glBegin(GL_TRIANGLES)

    for i in range(N - 1):
        for j in range(N - 1):
            p00 = jajo[i][j]
            p10 = jajo[i + 1][j]
            p11 = jajo[i + 1][j + 1]
            p01 = jajo[i][j + 1]

            for triangle in ((p00, p10, p11), (p00, p11, p01)):
                glColor3f(*_random_triangle_color(*triangle))
                for vertex in triangle:
                    glVertex3fv(vertex)

    glEnd()
    glShadeModel(GL_SMOOTH)


def generate_jajo_trianglestrip(N):
    if N < 2:
        return

    glShadeModel(GL_FLAT)

    for i in range(N - 1):
        strip = []
        glBegin(GL_TRIANGLE_STRIP)

        for j in range(N):
            for vertex in (jajo[i][j], jajo[i + 1][j]):
                strip.append(vertex)

                if len(strip) >= 3:
                    glColor3f(*_random_triangle_color(*strip[-3:]))

                glVertex3fv(vertex)

        glEnd()

    glShadeModel(GL_SMOOTH)


def generate_jajo_points(N):
    global jajo
    for i in range(0, N):
        u = i/(N-1)
        for j in range(0, N):
            v = j/(N-1)
            jajo[i][j][0] = xuv(u,v)
            jajo[i][j][1] = yuv(u,v)
            jajo[i][j][2] = zuv(u,v)
    

def xuv(u,v):
    return u*(u*(u*(u*(-90*u + 225) - 270) + 180) - 45) * cos(pi * v)

def yuv(u,v):
    return 160*u*u*(u*(u-2) + 1) - 5

def zuv(u,v):
    return u*(u*(u*(u*(-90*u + 225) - 270) + 180) - 45) * sin(pi * v)
    
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
    generate_jajo_points(N)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

N = 25
jajo = [[[0.0] * 3 for i in range(N)] for j in range(N)];

if __name__ == '__main__':
    main()
