import random

from glfw.GLFW import *
from OpenGL.GL import *

ZADANIE = 4.0  # Do wyboru: 3.0, 3.5, 4.0

ZIARNO = random.randint(0, 1000000)


def trojkat():
    glBegin(GL_TRIANGLES)

    glColor3f(1, 0, 0)
    glVertex2f(-70, -60)

    glColor3f(0, 1, 0)
    glVertex2f(70, -60)

    glColor3f(0, 0, 1)
    glVertex2f(0, 70)

    glEnd()


def prostokat(x, y, a, b, d=0):
    # Losowa zmiana szerokości i wysokości.
    # Dla d=0 wymiary pozostają bez zmian.
    a = a * (1 + random.uniform(-d, d))
    b = b * (1 + random.uniform(-d, d))

    glBegin(GL_TRIANGLES)

    # Pierwszy trójkąt
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)

    # Drugi trójkąt
    glVertex2f(x, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)

    glEnd()


def losowy_kolor():
    glColor3f(random.random(), random.random(), random.random())


def render():
    glClear(GL_COLOR_BUFFER_BIT)

    # Stały wygląd podczas przerysowywania okna.
    random.seed(ZIARNO)

    if ZADANIE == 3.0:
        trojkat()

    elif ZADANIE == 3.5:
        glColor3f(0, 0.7, 1)
        prostokat(-60, -40, 120, 80)

    elif ZADANIE == 4.0:
        losowy_kolor()
        prostokat(-60, -40, 120, 80, d=0.5)

    glFlush()


def update_viewport(window, width, height):
    width = max(1, width)
    height = max(1, height)
    proporcje = width / height

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if width <= height:
        glOrtho(
            -100, 100,
            -100 / proporcje, 100 / proporcje,
            -1, 1
        )
    else:
        glOrtho(
            -100 * proporcje, 100 * proporcje,
            -100, 100,
            -1, 1
        )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        return

    window = glfwCreateWindow(
        600, 600, "Laboratorium 2", None, None
    )

    if not window:
        glfwTerminate()
        return

    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)

    glfwSetFramebufferSizeCallback(window, update_viewport)

    width, height = glfwGetFramebufferSize(window)
    update_viewport(window, width, height)

    while not glfwWindowShouldClose(window):
        render()
        glfwSwapBuffers(window)
        glfwWaitEvents()

    glfwTerminate()

if __name__ == "__main__":
    main()