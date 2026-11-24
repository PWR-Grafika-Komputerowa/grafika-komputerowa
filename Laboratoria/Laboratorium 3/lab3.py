import math
import sys
import numpy as np

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 30
tab = np.zeros((N, N, 3))
colors = np.zeros((N, N, 3))

def generate_egg():
    global colors
    u_vals = np.linspace(0.0, 1.0, N)
    v_vals = np.linspace(0.0, 1.0, N)
    colors = np.random.rand(N, N, 3)

    colors[0, :] = colors[0, 0]
    colors[N - 1, :] = colors[0, 0]

    for i in range(N):
        colors[N - 1 - i, N - 1] = colors[i, 0]

    for i in range(N):
        u = u_vals[i]

        y = 160 * (u**4) - 320 * (u**3) + 160 * (u**2) - 5

        for j in range(N):
            v = v_vals[j]

            x = (-90 * (u**5) + 225 * (u**4) - 270 * (u**3) + 180 * (u**2) - 45 * u) * math.cos(math.pi * v)
            z = (-90 * (u**5) + 225 * (u**4) - 270 * (u**3) + 180 * (u**2) - 45 * u) * math.sin(math.pi * v)

            tab[i, j] = [x, y, z]

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def mid(p1, p2):
    return [(p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0, (p1[2] + p2[2]) / 2.0]


def draw_square_pyramid(v0, v1, v2, v3, v4):
    c0 = [1.0, 1.0, 1.0]
    c1 = [1.0, 0.0, 0.0]
    c2 = [0.0, 1.0, 0.0]
    c3 = [0.0, 0.0, 1.0]
    c4 = [1.0, 1.0, 0.0]

    glColor3fv(c0)
    glVertex3fv(v0)
    glColor3fv(c1)
    glVertex3fv(v1)
    glColor3fv(c2)
    glVertex3fv(v2)

    glColor3fv(c0)
    glVertex3fv(v0)
    glColor3fv(c2)
    glVertex3fv(v2)
    glColor3fv(c3)
    glVertex3fv(v3)

    glColor3fv(c0)
    glVertex3fv(v0)
    glColor3fv(c3)
    glVertex3fv(v3)
    glColor3fv(c4)
    glVertex3fv(v4)

    glColor3fv(c0)
    glVertex3fv(v0)
    glColor3fv(c4)
    glVertex3fv(v4)
    glColor3fv(c1)
    glVertex3fv(v1)

    glColor3fv(c1)
    glVertex3fv(v1)
    glColor3fv(c2)
    glVertex3fv(v2)
    glColor3fv(c3)
    glVertex3fv(v3)

    glColor3fv(c1)
    glVertex3fv(v1)
    glColor3fv(c3)
    glVertex3fv(v3)
    glColor3fv(c4)
    glVertex3fv(v4)


def sierpinski_pyramid(v0, v1, v2, v3, v4, depth):
    if depth == 0:
        draw_square_pyramid(v0, v1, v2, v3, v4)
        return

    m01, m02, m03, m04 = mid(v0, v1), mid(v0, v2), mid(v0, v3), mid(v0, v4)

    m12, m23, m34, m41 = mid(v1, v2), mid(v2, v3), mid(v3, v4), mid(v4, v1)

    c = mid(v1, v3)

    sierpinski_pyramid(v0, m01, m02, m03, m04, depth - 1)

    sierpinski_pyramid(m01, v1, m12, c, m41, depth - 1)
    sierpinski_pyramid(m02, m12, v2, m23, c, depth - 1)
    sierpinski_pyramid(m03, c, m23, v3, m34, depth - 1)
    sierpinski_pyramid(m04, m41, c, m34, v4, depth - 1)

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

    angle = time * 180.0 / math.pi
    spin(angle)
    axes()

# Rysowanie punktami
#     glBegin(GL_POINTS)
#     glColor3f(1.0, 1.0, 1.0)
#
#     for i in range(N):
#         for j in range(N):
#             glVertex3fv(tab[i, j])
#     glEnd()

# Rysowanie liniami
#     glBegin(GL_LINES)
#     glColor3f(1.0, 1.0, 1.0)
#     for i in range(N):
#         for j in range(N):
#             if i + 1 < N:
#                 glVertex3fv(tab[i, j])
#                 glVertex3fv(tab[i + 1, j])
#             if j + 1 < N:
#                 glVertex3fv(tab[i, j])
#                 glVertex3fv(tab[i, j + 1])
#     glEnd()


# Rysowanie trójkątami
#     glBegin(GL_TRIANGLES)
#     for i in range(N - 1):
#         for j in range(N - 1):
#             glColor3fv(colors[i, j])
#             glVertex3fv(tab[i, j])
#
#             glColor3fv(colors[i + 1, j])
#             glVertex3fv(tab[i + 1, j])
#
#             glColor3fv(colors[i, j + 1])
#             glVertex3fv(tab[i, j + 1])
#
#
#             glColor3fv(colors[i + 1, j])
#             glVertex3fv(tab[i + 1, j])
#
#             glColor3fv(colors[i + 1, j + 1])
#             glVertex3fv(tab[i + 1, j + 1])
#
#             glColor3fv(colors[i, j + 1])
#             glVertex3fv(tab[i, j + 1])
#     glEnd()

# Rysowanie paskami trójkątów
#     for i in range(N - 1):
#         glBegin(GL_TRIANGLE_STRIP)
#
#         for j in range(N):
#             glColor3fv(colors[i, j])
#             glVertex3fv(tab[i, j])
#
#             glColor3fv(colors[i + 1, j])
#             glVertex3fv(tab[i + 1, j])
#
#         glEnd()

# Ustawienia do ostrosłupu Sierpińskiego
#     v0 = [0.0, 3.5, 0.0]
#     v1 = [-3.0, -2.5, 3.0]
#     v2 = [3.0, -2.5, 3.0]
#     v3 = [3.0, -2.5, -3.0]
#     v4 = [-3.0, -2.5, -3.0]
#
#     glBegin(GL_TRIANGLES)
#     sierpinski_pyramid(v0, v1, v2, v3, v4, 1)
#     glEnd()

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