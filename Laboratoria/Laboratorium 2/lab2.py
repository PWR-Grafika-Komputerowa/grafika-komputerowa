import sys
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

DEFORMATION = 1

random.seed(10)

def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(-100.0, 100.0, -100.0, 100.0, -1.0, 1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_triangle():
    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-70.0, -50.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(70.0, -50.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 70.0)

    glEnd()

def draw_rectangle(x, y, a, b):

    left = x - a / 2
    right = x + a / 2
    bottom = y - b / 2
    top = y + b / 2

    glBegin(GL_TRIANGLES)

    glVertex2f(left, bottom)
    glVertex2f(right, bottom)
    glVertex2f(right, top)

    glVertex2f(left, bottom)
    glVertex2f(right, top)
    glVertex2f(left, top)

    glEnd()

def create_deformed_rectangle(x, y, a, b, d=0.0):
    d = max(0.0, min(d, 0.9))

    width = a * random.uniform(1.0 - d, 1.0 + d)
    height = b * random.uniform(1.0 - d, 1.0 + d)

    color1 = (
        random.random(),
        random.random(),
        random.random()
    )

    color2 = (
        random.random(),
        random.random(),
        random.random()
    )

    color3 = (
        random.random(),
        random.random(),
        random.random()
    )

    color4 = (
        random.random(),
        random.random(),
        random.random()
    )

    return {
        "x": x,
        "y": y,
        "a": width,
        "b": height,
        "colors": [color1, color2, color3, color4]
    }


def draw_deformed_rectangle(rect):
    x = rect["x"]
    y = rect["y"]
    a = rect["a"]
    b = rect["b"]
    c = rect["colors"]

    left = x - a / 2
    right = x + a / 2
    bottom = y - b / 2
    top = y + b / 2

    glBegin(GL_TRIANGLES)

    glColor3f(*c[0])
    glVertex2f(left, bottom)

    glColor3f(*c[1])
    glVertex2f(right, bottom)

    glColor3f(*c[2])
    glVertex2f(right, top)

    glColor3f(*c[0])
    glVertex2f(left, bottom)

    glColor3f(*c[2])
    glVertex2f(right, top)

    glColor3f(*c[3])
    glVertex2f(left, top)

    glEnd()

rect1 = create_deformed_rectangle(
    -45.0, 0.0, 35.0, 35.0, DEFORMATION
)

rect2 = create_deformed_rectangle(
    45.0, 0.0, 35.0, 35.0, DEFORMATION
)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    draw_triangle()

    glColor3f(1.0, 1.0, 1.0)
    draw_rectangle(0.0, -65.0, 25.0, 15.0)

    draw_deformed_rectangle(rect1)
    draw_deformed_rectangle(rect2)

    glFlush()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(
        800, 800,
        "Laboratorium OpenGL - zadania 3.0-4.0",
        None,
        None
    )

    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)

    startup()

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == "__main__":
    main()
