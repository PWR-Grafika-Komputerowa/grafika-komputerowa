from OpenGL.GLU import *
from OpenGL.GL import *
from glfw.GLFW import *
import sys
import random
random.seed()
a = random.random()
b = random.random()
c = random.random()
d = random.randint(0, 20) - random.randint(1,10) / 10
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

def main():
    x = int(input("Podaj współrzędną x prawego górnego wierzchołka: "))
    y = int(input("Podaj współrzędną y prawego górnego wierzchołka: "))
    a = int(input("Podaj długość boku a w pikselach: "))
    b = int(input("Podaj długość boku b w pikselach: "))
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
        render(glfwGetTime(), x, y, a, b)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

def render(time, x, y, l, m):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(a, b, c)
    glVertex2f(x + d, y - d)
    glVertex2f(x - l - d, y + d)
    glVertex2f(x + d, y - m - d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(a, b, c)
    glVertex2f(x - l - d, y - m + d)
    glVertex2f(x + d, y - m - d)
    glVertex2f(x - l - d,y + d)
    glEnd()
    glFlush()

if __name__ == '__main__':
    main()