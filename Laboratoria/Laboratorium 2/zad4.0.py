import sys
import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
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

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def draw_rectangle_deformed(x, y, a, b, d=0.0):
    a = a * (1.0 + random.uniform(-d, d))
    b = b * (1.0 + random.uniform(-d, d))

    glBegin(GL_TRIANGLES)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y + b)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y + b)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y + b)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    random.seed(42)
    draw_rectangle_deformed(-40.0, -40.0, 80.0, 80.0, d=0.2)

    glFlush()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Zadanie 4.0", None, None)
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