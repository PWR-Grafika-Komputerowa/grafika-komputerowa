import sys
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

def draw_rectangle(x, y, a, b):
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)

    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)
    glEnd()

def draw_sierpinski(x, y, size, level):
    if level == 0:
        draw_rectangle(x, y, size, size)
    else:
        new_size = size / 3.0
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                draw_sierpinski(x + i * new_size, y + j * new_size, new_size, level - 1)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.8, 0.2, 0.2)
    draw_sierpinski(-80.0, -80.0, 160.0, 3)

    glFlush()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Zadanie 4.5", None, None)
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