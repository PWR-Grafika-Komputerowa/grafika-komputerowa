#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Vec2:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __truediv__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def random_color():
    r = random.randint(0, 256)
    g = random.randint(0, 256)
    b = random.randint(0, 256)
    return r, g, b


R_RECT, G_RECT, B_RECT = random_color()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    
    if len(sys.argv) == 1:
        # zadanie (1)
        glBegin(GL_TRIANGLES)

        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(-50.0, 0.0)

        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(50.0, 0.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex2f(0.0, 50.0)

        glEnd()

        draw_rectangle(0, -20, 100, 40, color_flag=True)

        glFlush()
    elif len(sys.argv) == 3 and sys.argv[1].lower() == "carpet":
        center = Vec2(0.0, 0.0)
        base_width = 150.0
        base_height = 100.0
        level = int(sys.argv[2])
        draw_rectangle(center.x, center.y, base_width, base_height, color_flag=True)
        sierpinski_carpet(center, base_width, base_height, level)
    elif len(sys.argv) == 3 and sys.argv[1].lower() == "triangle":
        center = Vec2(0.0, 0.0)
        edge_length = 150.0
        level = int(sys.argv[2])
        draw_triangle(center, edge_length, black_color=True)
        sierpinski_triangle(center, edge_length, level)
    else:
        print("Invalid arguments. If you wish to run fractals, please use: 'carpet <level>' or 'triangle <level>' as arguments.")
        sys.exit(1)


# zadanie (2), zadanie (3)
def draw_rectangle(x, y, a, b, d=0, color_flag=False):  # a - width, b - height, d - deformation
    random.seed(123)

    top_left = Vec2(x - a / 2, y + b / 2)
    bot_left = Vec2(x - a / 2, y - b / 2)
    top_right = Vec2(x + a / 2, y + b / 2)
    bot_right = Vec2(x + a / 2, y - b / 2)

    top_left = top_left + Vec2(random.uniform(-d, d), random.uniform(-d, d))
    bot_left = bot_left + Vec2(random.uniform(-d, d), random.uniform(-d, d))
    top_right = top_right + Vec2(random.uniform(-d, d), random.uniform(-d, d))
    bot_right = bot_right + Vec2(random.uniform(-d, d), random.uniform(-d, d))

    global R_RECT, G_RECT, B_RECT

    glBegin(GL_TRIANGLES)

    if color_flag:
        glColor3f(R_RECT / 255.0, G_RECT / 255.0, B_RECT / 255.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    glVertex2f(top_left.x, top_left.y)
    glVertex2f(bot_left.x, bot_left.y)
    glVertex2f(top_right.x, top_right.y)

    glVertex2f(bot_right.x, bot_right.y)
    glVertex2f(bot_left.x, bot_left.y)
    glVertex2f(top_right.x, top_right.y)

    glEnd()


# zadanie (4)
def sierpinski_carpet(center, width, height, level):
    if level == 0:
        return

    new_width = width / 3.0
    new_height = height / 3.0

    draw_rectangle(center.x, center.y, new_width, new_height, 0)

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            new_center = center + Vec2(dx * new_width, dy * new_height)
            sierpinski_carpet(new_center, new_width, new_height, level - 1)


# zadanie (5)
def draw_triangle(center, edge_length, black_color=False):
    h = edge_length * 3**0.5 / 2.0
    vertex1 = Vec2(center.x, center.y + 2 * h / 3.0)
    vertex2 = Vec2(center.x - edge_length / 2, center.y - h / 3.0)
    vertex3 = Vec2(center.x + edge_length / 2, center.y - h / 3.0)

    glBegin(GL_TRIANGLES)
    if black_color:
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 0.0, 0.0)
    glVertex2f(vertex1.x, vertex1.y)
    glVertex2f(vertex2.x, vertex2.y)
    glVertex2f(vertex3.x, vertex3.y)
    glEnd()


def sierpinski_triangle(center, edge_length, level):
    if level == 0:
        draw_triangle(center, edge_length, black_color=False)
        return

    new_edge = edge_length / 2.0
    h_small = new_edge * 3**0.5 / 2.0

    sierpinski_triangle(center + Vec2(0, 2 * h_small / 3.0), new_edge, level - 1)
    sierpinski_triangle(center + Vec2(-new_edge / 2.0, -h_small / 3.0), new_edge, level - 1)
    sierpinski_triangle(center + Vec2(new_edge / 2.0, -h_small / 3.0), new_edge, level - 1)
 

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
