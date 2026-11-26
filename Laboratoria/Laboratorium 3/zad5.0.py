import sys
import math

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

R = 0.85  # odleglosc srodka torusa od srodka rurki.
r = 0.22  # promien rurki.
PODZIALY_U = 32
PODZIALY_V = 16
LICZBA_OGNIW = 7


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


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


def torus_punkt(u, v):
    x = (R + r * math.cos(2 * math.pi * v)) * math.cos(2 * math.pi * u)
    y = (R + r * math.cos(2 * math.pi * v)) * math.sin(2 * math.pi * u)
    z = r * math.sin(2 * math.pi * v)
    return x, y, z


def rysuj_torus(kolor):
    # kazdy pasek tworzy kolejny fragment rurki.
    for i in range(PODZIALY_U):
        u1 = i / PODZIALY_U
        u2 = (i + 1) / PODZIALY_U
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(PODZIALY_V + 1):
            v = j / PODZIALY_V
            jasnosc = 0.7 + 0.3 * math.cos(2 * math.pi * v)
            glColor3f(*(skladowa * jasnosc for skladowa in kolor))
            glVertex3fv(torus_punkt(u1, v))
            glVertex3fv(torus_punkt(u2, v))
        glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    axes()
    glRotatef(15, 1, 0, 0)
    glRotatef(time * 15, 0, 1, 0)

    for i in range(LICZBA_OGNIW):
        glPushMatrix()
        x = (i - (LICZBA_OGNIW - 1) / 2) * 1.4
        y = 0.6 * math.sin((i - (LICZBA_OGNIW - 1) / 2) * 0.65)
        glTranslatef(x, y, 0)
        if i % 2 == 0:
            glRotatef(25, 1, 0, 0)
            kolor = (0.95, 0.65, 0.15)
        else:
            glRotatef(-65, 1, 0, 0)
            kolor = (0.25, 0.75, 0.95)
        rysuj_torus(kolor)
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
