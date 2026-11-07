
#!/usr/bin/env python3
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *



# numer wybranego zadania
wybor = 1

# losowy kolor i wielkosc deformacji prostokata
kolor = (0.2, 0.7, 0.9)
deformacja = 0.0


# zadanie 3.0- rysowanie trojkata z trzema kolorami
def trojkat():
    glBegin(GL_TRIANGLES)

    # pierwszy wierzcholek - kolor czerwony
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-70.0, -60.0)

    # drugi wierzcholek - kolor zielony
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(70.0, -60.0)

    # trzeci wierzcholek - kolor niebieski
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 70.0)

    glEnd()


# zadanie 3.5 i 4.0 - prostokat z dwoch trojkatow

def prostokat(x, y, a, b, d=0.0, kolor=(0.2, 0.7, 0.9)):
    # wyznaczenie czterech wierzcholkow (x i y = srodek prostokata, a = szerokosc, b = wysokosc)
    punkty = [
        (x - a/2, y - b/2),
        (x + a/2, y - b/2),
        (x + a/2, y + b/2),
        (x - a/2, y + b/2)
    ]

    # zadanie 4.0- losowe przesuniecie wierzcholkow
    if d > 0:
        punkty = [
            (px + random.uniform(-d, d),
             py + random.uniform(-d, d))
            for px, py in punkty
        ]

    glColor3f(*kolor)    # ustawienie koloru prostokata
    glBegin(GL_TRIANGLES)    # rysowanie prostokata za pomoca dwoch trojkatow


    # pierwszy trojkat
    glVertex2f(*punkty[0])
    glVertex2f(*punkty[1])
    glVertex2f(*punkty[2])

    # drugi trojkat
    glVertex2f(*punkty[0])
    glVertex2f(*punkty[2])
    glVertex2f(*punkty[3])

    glEnd()


# zadanie 4.5-dywan sierpinskiego
def dywan(x, y, s, poziom):
    # warunek konca rekurencji: rysowanie kwadratu
    if poziom == 0:
        glBegin(GL_QUADS)
        glVertex2f(x - s/2, y - s/2)
        glVertex2f(x + s/2, y - s/2)
        glVertex2f(x + s/2, y + s/2)
        glVertex2f(x - s/2, y + s/2)
        glEnd()
        return

    # podzial kwadratu na dziewiec czesci
    krok = s / 3

    for i in range(3):
        for j in range(3):

            # pominiecie srodkowej czesci
            if i == 1 and j == 1:
                continue

            # wyznaczenie srodka mniejszego kwadratu
            nx = x - s/2 + krok/2 + j*krok
            ny = y - s/2 + krok/2 + i*krok

            # powtorzenie podzialu dla mniejszego kwadratu
            dywan(nx, ny, krok, poziom - 1)


# zadanie 5.0- trojkat sierpinskiego
def sierpinski(a, b, c, poziom):
    # warunek konca rekurencji: rysowanie trojkata
    if poziom == 0:
        glVertex2f(*a)
        glVertex2f(*b)
        glVertex2f(*c)
        return

    # obliczenie srodkow bokow
    ab = ((a[0] + b[0])/2, (a[1] + b[1])/2)
    bc = ((b[0] + c[0])/2, (b[1] + c[1])/2)
    ca = ((c[0] + a[0])/2, (c[1] + a[1])/2)

    # rekurencyjne rysowanie trzech mniejszych trojkatow
    sierpinski(a, ab, ca, poziom - 1)
    sierpinski(ab, b, bc, poziom - 1)
    sierpinski(ca, bc, c, poziom - 1)


# inicjalizacja programu
def startup():
    # ustawienie poczatkowego obszaru rysowania
    update_viewport(None, 400, 400)

    # ustawienie szarego tla
    glClearColor(0.5, 0.5, 0.5, 1.0)


# rysowanie wybranego zadania
def render(time):
    # wyczyszczenie poprzedniej klatki
    glClear(GL_COLOR_BUFFER_BIT)

    # zadanie 3.0: trojkat w trzech kolorach
    if wybor == 1:
        trojkat()

    # zadanie 3.5: zwykly prostokat
    elif wybor == 2:
        prostokat(0.0, 0.0, 120.0, 80.0)

    # zadanie 4.0: prostokat z losowym kolorem i deformacja
    elif wybor == 3:
        prostokat(0.0, 0.0, 120.0, 80.0, 1.0, kolor)

    # zadanie 4.5: dywan sierpinskiego
    elif wybor == 4:
        glColor3f(0.2, 0.7, 0.9)
        dywan(0.0, 0.0, 160.0, 3)

    # zadanie 5.0: trojkat sierpinskiego
    elif wybor == 5:
        glColor3f(0.2, 0.7, 0.9)
        glBegin(GL_TRIANGLES)
        sierpinski((-85.0, -70.0), (85.0, -70.0),
                   (0.0, 80.0), 5)
        glEnd()

    # wyslanie polecen rysowania
    glFlush()


# dopasowanie projekcji do rozmiaru okna
def update_viewport(window, width, height):
    # zabezpieczenie przed dzieleniem przez zero
    if width == 0:
        width = 1
    if height == 0:
        height = 1

    # obliczenie proporcji okna
    aspect_ratio = width / height

    # ustawienie projekcji
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    # zachowanie proporcji figur po zmianie rozmiaru okna
    if width <= height:
        glOrtho(-100.0, 100.0,
                -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio,
                -100.0, 100.0, 1.0, -1.0)

    # powrot do macierzy modelowania
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# zamkniecie programu
def shutdown():
    pass


# funkcja glowna
def main():
    global wybor, kolor, deformacja

    # pobranie numeru zadania
    try:
        wybor = int(input(
            "1 - trojkat z trzema kolorami\n"
            "2 - prostokat\n"
            "3 - prostokat z deformacja\n"
            "4 - dywan sierpinskiego\n"
            "5 - trojkat sierpinskiego\n"
            "Wybor: "
        ))
    except ValueError:
        print("Podaj liczbe od 1 do 5.")
        sys.exit(-1)

    # sprawdzenie poprawnosci wyboru
    if wybor not in range(1, 6):
        print("Podaj liczbe od 1 do 5.")
        sys.exit(-1)

    # losowanie koloru i deformacji tylko dla zadania 4.0
    kolor = (random.random(), random.random(), random.random())
    deformacja = random.uniform(0.0, 8.0)

    # uruchomienie glfw
    if not glfwInit():
        sys.exit(-1)

    # utworzenie okna
    window = glfwCreateWindow(400, 400, "Figury i fraktale", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    # ustawienie aktywnego okna i obslugi zmiany rozmiaru
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    # wykonanie ustawien poczatkowych
    startup()

    # glowna petla programu
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    # zakonczenie programu
    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()
