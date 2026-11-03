
from OpenGL.GLU import *
from OpenGL.GL import *
from glfw.GLFW import *
import sys

x = 180
y = 180


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)


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
    # Liczba iteracji podawana przez użytkownika
    poziom = int(input("Podaj liczbę iteracji (0-5): "))

    if poziom < 0 or poziom > 5:
        print("Podaj liczbę od 0 do 5!")
        return

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
        render(glfwGetTime(), poziom)
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()


def render(time, poziom):
    glClear(GL_COLOR_BUFFER_BIT)

    # Początkowy kwadrat
    kwadraty = [(-x/2, -y/2, x)]

    # Kolejne iteracje
    for k in range(poziom):

        nowe_kwadraty = []

        # Dzielimy wszystkie istniejące kwadraty
        for a, b, bok in kwadraty:

            maly_bok = bok / 3

            for i in range(3):
                for j in range(3):

                    # Pomijamy środkowy kwadrat
                    if i == 1 and j == 1:
                        continue

                    # Współrzędne nowego kwadratu
                    nx = a + i * maly_bok
                    ny = b + j * maly_bok

                    nowe_kwadraty.append((nx, ny, maly_bok))

        kwadraty = nowe_kwadraty

    # Rysowanie pozostałych kwadratów
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.35)

    for a, b, bok in kwadraty:

        # Pierwszy trójkąt
        glVertex2f(a, b)
        glVertex2f(a + bok, b)
        glVertex2f(a, b + bok)

        # Drugi trójkąt
        glVertex2f(a + bok, b)
        glVertex2f(a + bok, b + bok)
        glVertex2f(a, b + bok)

    glEnd()
    glFlush()


if __name__ == '__main__':
    main()
