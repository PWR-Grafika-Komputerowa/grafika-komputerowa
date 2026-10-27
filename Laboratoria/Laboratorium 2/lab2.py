import sys
import random
import time

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

RAND_SEED = time.time()

def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    update_viewport(None, 400, 400)

def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

# Trójkąt z każdym wierzchołkiem innego koloru
    # glColor3f(1.0, 0.0, 0.0)
    # glBegin(GL_TRIANGLES)
    # glVertex2f(50.0, 0.0)
    # glColor3f(0.0, 1.0, 0.0)
    # glVertex2f(-50.0, 0.0)
    # glColor3f(0.0, 0.0, 1.0)
    # glVertex2f(0.0, 50.0)
    # glEnd()

# Prostokąt
#     draw_rectangle(0, 0, 100, 75)

# Prostokąt z elementami losowości
#     random_rectangle(0, 0, 50, 25, 0.4)

# Fraktal
#     draw_fractal(0, 0, 100, 100, 3)

# Trójkąt Sierpińskiego
    # draw_sierpinski_triangle(0.0, 0.0, 100, 100, 4)

    glFlush()

def draw_rectangle(x, y, a, b):

    width_a = a / 2.0
    height_b = b / 2.0

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - width_a, y - height_b)
    glVertex2f(x + width_a, y - height_b)
    glVertex2f(x - width_a, y + height_b)

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x + width_a, y + height_b)
    glVertex2f(x - width_a, y + height_b)
    glVertex2f(x + width_a, y - height_b)
    glEnd()

def random_rectangle(x, y, a, b, d=0.0):
    random.seed(RAND_SEED)
    a_random = 1.0 + (random.random() - 0.5) * d
    b_random = 1.0 + (random.random() - 0.5) * d

    width_a = a * a_random
    height_b = b * b_random

    r_col = random.random()
    g_col = random.random()
    b_col = random.random()

    glColor3f(r_col, g_col, b_col)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - width_a, y - height_b)
    glVertex2f(x + width_a, y - height_b)
    glVertex2f(x - width_a, y + height_b)

    r_col = random.random()
    g_col = random.random()
    b_col = random.random()

    glColor3f(r_col, g_col, b_col)
    glVertex2f(x + width_a, y + height_b)
    glVertex2f(x - width_a, y + height_b)
    glVertex2f(x + width_a, y - height_b)
    glEnd()


def draw_fractal(x, y, a, b, depth):
    if depth == 0:
        draw_rectangle(x, y, a, b)
        return

    w = a / 3.0
    h = b / 3.0

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            draw_fractal(x + i * w, y + j * h, w, h, depth - 1)

def draw_triangle(x, y, a, b):
    width_a = a / 2.0
    height_b = b / 2.0

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - width_a, y - height_b)
    glVertex2f(x + width_a, y - height_b)
    glVertex2f(x, y + height_b)
    glEnd()

def draw_sierpinski_triangle(x, y, a, b, depth):
    if depth == 0:
        draw_triangle(x, y, a, b)
        return

    w = a / 2.0
    h = b / 2.0

    draw_sierpinski_triangle(x - w / 2.0, y - h / 2.0, w, h, depth - 1)
    draw_sierpinski_triangle(x + w / 2.0, y - h / 2.0, w, h, depth - 1)
    draw_sierpinski_triangle(x, y + h / 2.0, w, h, depth - 1)

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
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)

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