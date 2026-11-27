#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *

ZAD = 1

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

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

def zad1():
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 1.0, 0.2)
    glVertex2f(-50.0, -50.0)

    glColor3f(1.0, 0.3, 0.7)
    glVertex2f(50.0, -50.0)

    glColor3f(0.2, 1.0, 1.0)
    glVertex2f(0.0, 50.0)
    glEnd()

def zad2(x, y, a, b):
    bl = (x - a/2, y - b/2)  # bottom left
    tl = (x - a/2, y + b/2)  # top left
    tr = (x + a/2, y + b/2)  # top right
    br = (x + a/2, y - b/2)  # bottom right

    glColor3f(0.5, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(bl[0], bl[1])
    glVertex2f(tl[0], tl[1])
    glVertex2f(tr[0], tr[1])
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(bl[0], bl[1])
    glVertex2f(tr[0], tr[1])
    glVertex2f(br[0], br[1])
    glEnd()

def zad3(x, y, a, b, d):
    if not hasattr(zad3, "losowe"):
        zad3.losowe = (
            random.uniform(1 - d, 1 + d),
            random.uniform(1 - d, 1 + d),
            random.random(),
            random.random(),
            random.random()
        )

    rand_a, rand_b, red, green, blue = zad3.losowe
    a = a * rand_a
    b = b * rand_b

    bl = (x - a/2, y - b/2)  # bottom left
    tl = (x - a/2, y + b/2)  # top left
    tr = (x + a/2, y + b/2)  # top right
    br = (x + a/2, y - b/2)  # bottom right

    glColor3f(red, green, blue)


    glBegin(GL_TRIANGLES)
    glVertex2f(bl[0], bl[1])
    glVertex2f(tl[0], tl[1])
    glVertex2f(tr[0], tr[1])

    glVertex2f(bl[0], bl[1])
    glVertex2f(tr[0], tr[1])
    glVertex2f(br[0], br[1])
    glEnd()

def zad4(x, y, a, b, d):
    if d == 0:
        zad2(x, y, a, b)
        return

    nowe_a = a / 3
    nowe_b = b / 3

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue

            nowe_x = x + (i-1) * nowe_a
            nowe_y = y + (j-1) * nowe_b

            zad4(nowe_x, nowe_y, nowe_a, nowe_b, d - 1)
def zad5(x1, y1, x2, y2, x3, y3, d):
    if not hasattr(zad5, "kolory"):
        zad5.kolory = {}

    if d == 0:
        trojkat = (x1, y1, x2, y2, x3, y3)

        if trojkat not in zad5.kolory:
            zad5.kolory[trojkat] = (
                random.random(),
                random.random(),
                random.random()
            )

        red, green, blue = zad5.kolory[trojkat]
        glColor3f(red, green, blue)

        glBegin(GL_TRIANGLES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glVertex2f(x3, y3)
        glEnd()
        return

    #środki boków
    sx12 = (x1 + x2) / 2
    sy12 = (y1 + y2) / 2

    sx23 = (x2 + x3) / 2
    sy23 = (y2 + y3) / 2

    sx31 = (x3 + x1) / 2
    sy31 = (y3 + y1) / 2


    zad5(x1, y1, sx12, sy12, sx31, sy31, d - 1)
    zad5(sx12, sy12, x2, y2, sx23, sy23, d - 1)
    zad5(sx31, sy31, sx23, sy23, x3, y3, d - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    if ZAD == 1:
        zad1()
    if ZAD == 2:
        #a to góra, b to bok
        zad2(0, 0, 100, 50)
    if ZAD == 3:
        zad3(0, 0, 100, 50, 0.9)
    if ZAD == 4:
        zad4(0, 0, 100, 50, 3)
    if ZAD == 5:
        zad5(-80, -70, 80, -70, 0, 80, 3)
    glFlush()

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