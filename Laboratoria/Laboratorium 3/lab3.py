
#!/usr/bin/env python3

import sys, math
import numpy as np

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

# liczba punktow w kazdym kierunku parametrycznym
N = 20

# numer wybranego zadania
zadanie = 1

# rownania parametryczne jajka
x = lambda u, v: (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
y = lambda u, v: 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
z = lambda u, v: (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

# tablice kolorow
kolory = np.zeros((N, N, 3))
kolory_torus = np.zeros((N, N, 3))


# generowanie i zamykanie kolorow
def add_colors():
    global kolory, kolory_torus

    kolory = np.random.rand(N, N, 3)

    # zamkniecie pierwszej i ostatniej kolumny jajka
    for i in range(N):
          kolory[N - 1 - i, N - 1] = kolory[i, 0]

    # jednakowe kolory na koncach jajka
    for j in range(N):
        kolory[0][j] = kolory[0][0]
        kolory[N-1][j] = kolory[0][0]

    # losowe kolory torusa
    kolory_torus = np.random.rand(N, N, 3)

    # zamkniecie pierwszej i ostatniej kolumny torusa
    for i in range(N):
        kolory_torus[i][N-1] = kolory_torus[i][0]

    # zamkniecie pierwszego i ostatniego wiersza torusa
    for j in range(N):
        kolory_torus[N-1][j] = kolory_torus[0][j]


def startup():
    # przygotowanie widoku i ustawien OpenGL
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glPointSize(3.0)


def shutdown():
    pass


# obrot modelu wokol osi x y oraz z
def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


# rysowanie osi ukladu wspolrzednych
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


# ustawienie koloru i wspolrzednych wierzcholka
def vertex(tab, kolory, i, j):
    glColor3fv(kolory[i][j])
    glVertex3fv(tab[i][j])


# rysowanie jajka
def Jajko():
    tab = np.zeros((N, N, 3))

    u, v = np.linspace(0, 1, N), np.linspace(0, 1, N)

    # obliczanie wspolrzednych wierzcholkow
    for i in range(N):
        for j in range(N):
            tab[i][j][0] = x(u[i], v[j])
            tab[i][j][1] = y(u[i], v[j])
            tab[i][j][2] = z(u[i], v[j])

    if zadanie == 1:
        # zadanie 1 - rysowanie punktow
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)

        for i in range(N):
            for j in range(N):
                glVertex3fv(tab[i][j])

        glEnd()

    elif zadanie == 2:
        # zadanie 2 - rysowanie linii
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_LINES)

        for i in range(N):
            for j in range(N):

                if i < N - 1:
                    glVertex3fv(tab[i][j])
                    glVertex3fv(tab[i + 1][j])

                if j < N - 1:
                    glVertex3fv(tab[i][j])
                    glVertex3fv(tab[i][j + 1])

        glEnd()

    elif zadanie == 3:
        # zadanie 3 - trojkaty
        glBegin(GL_TRIANGLES)

        for i in range(N - 1):
            for j in range(N - 1):

                vertex(tab, kolory, i, j)
                vertex(tab, kolory, i + 1, j)
                vertex(tab, kolory, i, j + 1)

                vertex(tab, kolory, i + 1, j)
                vertex(tab, kolory, i + 1, j + 1)
                vertex(tab, kolory, i, j + 1)

        glEnd()

    elif zadanie == 4:
        # zadanie 4 - paski trojkatow
        glShadeModel(GL_FLAT)

        for i in range(N - 1):
            glBegin(GL_TRIANGLE_STRIP)

            for j in range(N):
                glColor3fv(kolory[i][j])
                glVertex3fv(tab[i][j])

                glColor3fv(kolory[i + 1][j])
                glVertex3fv(tab[i + 1][j])

            glEnd()


# dodatkowy model torusa
def model_dodatkowy():
    tab = np.zeros((N, N, 3))
    u, v = np.linspace(0, 1, N), np.linspace(0, 1, N)

    R = 3.0
    r = 1.2

    # obliczanie wspolrzednych torusa
    for i in range(N):
        for j in range(N):
            tab[i][j][0] = (R + r * math.cos(2 * math.pi * v[j])) * math.cos(2 * math.pi * u[i])
            tab[i][j][1] = r * math.sin(2 * math.pi * v[j])
            tab[i][j][2] = (R + r * math.cos(2 * math.pi * v[j])) * math.sin(2 * math.pi * u[i])

    # zadanie 5 - kolorowe paski trojkatow
    glShadeModel(GL_SMOOTH)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)

        for j in range(N):
            glColor3fv(kolory_torus[i][j])
            glVertex3fv(tab[i][j])

            glColor3fv(kolory_torus[i + 1][j])
            glVertex3fv(tab[i + 1][j])

        glEnd()


def render(time):
    # wyczyszczenie poprzedniej klatki
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # obracanie modelu
    if zadanie >= 2:
        spin(time * 180 / math.pi)

    # rysowanie osi
    axes()

    if zadanie == 5:
        model_dodatkowy()
    else:
        Jajko()

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
        glOrtho(
            -7.5, 7.5,
            -7.5 / aspect_ratio, 7.5 / aspect_ratio,
            7.5, -7.5
        )
    else:
        glOrtho(
            -7.5 * aspect_ratio, 7.5 * aspect_ratio,
            -7.5, 7.5,
            7.5, -7.5
        )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    global zadanie

    # pobranie numeru zadania
    zadanie = 0

    while zadanie not in (1, 2, 3, 4, 5):
        try:
            zadanie = int(input("wybierz zadanie (1-5): "))
        except ValueError:
            pass

    # inicjalizacja GLFW
    if not glfwInit():
        sys.exit(-1)

    # utworzenie okna
    window = glfwCreateWindow(400, 400, __file__, None, None)

    if not window:
        glfwTerminate()
        sys.exit(-1)

    # aktywacja kontekstu OpenGL
    glfwMakeContextCurrent(window)

    # generowanie kolorow
    add_colors()

    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()

    # glowna petla programu
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()
