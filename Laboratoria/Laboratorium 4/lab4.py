#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


# wybor zadania
task = 1

# polozenie kamery
viewer = [0.0, 0.0, 10.0]

# katy obrotu i skala obiektu
theta = 0.0
phi = 0.0
scale = 1.0

# katy i odleglosc kamery orbitalnej
camera_theta = 0.0
camera_phi = 20.0
R = 10.0

# polozenie i kierunek kamery pierwszoosobowej
fly_pos = [0.0, 0.0, 8.0]
fly_yaw = -90.0
fly_pitch = 0.0
last_time = 0.0

# stan przyciskow myszy
left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

# poprzednia pozycja myszy
mouse_x_pos_old = 0.0
mouse_y_pos_old = 0.0

# przesuniecie myszy
delta_x = 0.0
delta_y = 0.0

# przelicznik pikseli na kat
pix2angle = 1.0

# tryb pracy w zadaniu 4
object_mode = False


# wybor zadania
def choose_task():
    print("\nLaboratorium 4")
    print("1 - 3.0 obrot obiektu")
    print("2 - 3.5 obrot i skalowanie")
    print("3 - 4.0 kamera orbitalna")
    print("4 - 4.5 kamera i zmiana trybow")
    print("5 - 5.0 kamera pierwszoosobowa")

    # sprawdzanie poprawnosci wyboru
    while True:
        answer = input("Wybierz zadanie (1-5): ")

        if answer in ("1", "2", "3", "4", "5"):
            return int(answer)

        print("Wpisz cyfre od 1 do 5")


# ustawienie tla i testu glebokosci
def startup():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


# funkcja konczaca program
def shutdown():
    pass


# rysowanie osi ukladu wspolrzednych
def axes():
    glBegin(GL_LINES)

    # os x w kolorze czerwonym
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    # os y w kolorze zielonym
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    # os z w kolorze niebieskim
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


# rysowanie przykladowego obiektu
def example_object():
    glColor3f(1.0, 1.0, 1.0)

    # utworzenie obiektu pomocniczego do rysowania
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)

    # ustawienie polozenia kuli
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    # rysowanie kuli
    gluSphere(quadric, 1.5, 10, 10)

    # rysowanie gornego walca
    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    # rysowanie dolnego walca
    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    # rysowanie pierwszego bocznego walca
    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    # rysowanie drugiego bocznego walca
    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    # przywrocenie poczatkowego polozenia
    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)

    # usuniecie obiektu pomocniczego
    gluDeleteQuadric(quadric)


# obrot obiektu i skalowanie
def object_view(use_scale):
    global theta, phi, scale

    # ustawienie kamery przed obiektem
    gluLookAt(0.0, 0.0, 10.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

    # aktualizacja katow obrotu
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    # obrot wokol osi x i y
    glRotatef(phi, 1.0, 0.0, 0.0)
    glRotatef(theta, 0.0, 1.0, 0.0)

    # skalowanie obiektu
    if use_scale:
        if right_mouse_button_pressed:
            scale += delta_y * 0.01
            scale = max(0.2, min(3.0, scale))

        glScalef(scale, scale, scale)


# ruch kamery wokol obiektu
def camera_orbit(limit):
    global camera_theta, camera_phi, R

    # zmiana katow kamery
    if left_mouse_button_pressed:
        camera_theta += delta_x * pix2angle
        camera_phi += delta_y * pix2angle

    # zmiana odleglosci kamery
    if right_mouse_button_pressed:
        R += delta_y * 0.05

    # ograniczenia ruchu kamery w zadaniu 4.5
    if limit:
        R = max(3.0, min(R, 30.0)) # zakres

        # ograniczenie katow do zakresu 0-360
        camera_theta %= 360.0
        camera_phi %= 360.0

        # unikniecie ustawienia kamery pionowo
        if abs(camera_phi - 90.0) < 0.5:
            camera_phi = 90.5

        if abs(camera_phi - 270.0) < 0.5:
            camera_phi = 270.5
    else:
        R = max(1.0, R)

    # zamiana katow na radiany
    t = math.radians(camera_theta)
    p = math.radians(camera_phi)

    # obliczenie polozenia kamery
    x = R * math.cos(t) * math.cos(p)
    y = R * math.sin(p)
    z = R * math.sin(t) * math.cos(p)

    # zmiana kierunku pionowego kamery
    up = 1.0

    if limit and 90.0 < camera_phi < 270.0:
        up = -1.0

    # skierowanie kamery na srodek obiektu
    gluLookAt(x, y, z,
              0.0, 0.0, 0.0,
              0.0, up, 0.0)


# sterowanie kamera pierwszoosobowa
def free_camera(window, dt):
    global fly_yaw, fly_pitch

    # zmiana kierunku patrzenia za pomoca myszy
    if left_mouse_button_pressed:
        fly_yaw += delta_x * pix2angle
        fly_pitch -= delta_y * pix2angle

        # ograniczenie kata patrzenia w gore i w dol
        fly_pitch = max(-89.0, min(89.0, fly_pitch))

    # zamiana katow na radiany
    yaw = math.radians(fly_yaw)
    pitch = math.radians(fly_pitch)

    # obliczenie kierunku patrzenia
    x = math.cos(yaw) * math.cos(pitch)
    y = math.sin(pitch)
    z = math.sin(yaw) * math.cos(pitch)

    # obliczenie kierunku ruchu w prawo
    right_x = -z
    right_z = x

    length = math.hypot(right_x, right_z)

    # normalizacja kierunku ruchu
    if length > 0:
        right_x /= length
        right_z /= length

    # obliczenie przesuniecia kamery
    step = 3.0 * dt #odległość ruchu kamery - jest zależna od czasu dt(prędkość ruchu nie zależy od liczby klatek na sekundę)

    # ruch do przodu
    if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
        fly_pos[0] += x * step
        fly_pos[1] += y * step
        fly_pos[2] += z * step

    # ruch do tylu
    if glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
        fly_pos[0] -= x * step
        fly_pos[1] -= y * step
        fly_pos[2] -= z * step

    # ruch w prawo
    if glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS:
        fly_pos[0] += right_x * step
        fly_pos[2] += right_z * step

    # ruch w lewo
    if glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS:
        fly_pos[0] -= right_x * step
        fly_pos[2] -= right_z * step

    # ustawienie kamery w kierunku patrzenia
    gluLookAt(fly_pos[0], fly_pos[1], fly_pos[2],
              fly_pos[0] + x, fly_pos[1] + y, fly_pos[2] + z,
              0.0, 1.0, 0.0)


# wyswietlanie jednej klatki
def render(time, window):
    global delta_x, delta_y, last_time

    # obliczenie czasu od poprzedniej klatki
    dt = time - last_time
    last_time = time

    # czyszczenie buforow i macierzy
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # wybor aktywnego zadania
    if task == 1:
        object_view(False)

    elif task == 2:
        object_view(True)

    elif task == 3:
        camera_orbit(False)

    elif task == 4:
        if object_mode:
            object_view(True)
        else:
            camera_orbit(True)

    elif task == 5:
        free_camera(window, dt)

    # wyzerowanie przesuniecia myszy
    delta_x = 0.0
    delta_y = 0.0

    # rysowanie osi i obiektu
    axes()
    example_object()

    glFlush()


# ustawienie projekcji po zmianie rozmiaru okna
def update_viewport(window, width, height):
    global pix2angle

    # sprawdzenie rozmiaru okna
    if width == 0 or height == 0:
        return

    # przeliczanie ruchu myszy na kat
    pix2angle = 360.0 / width

    # ustawienie macierzy projekcji
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # ustawienie perspektywy
    gluPerspective(70.0, width / height, 0.1, 300.0)

    glViewport(0, 0, width, height)

    # powrot do macierzy modelowania
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# obsluga klawiatury
def keyboard_key_callback(window, key, scancode, action, mods):
    global object_mode

    # zamkniecie programu klawiszem escape
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    # przelaczanie trybu kamera i obiekt
    if key == GLFW_KEY_C and action == GLFW_PRESS and task == 4:
        object_mode = not object_mode

        if object_mode:
            print("Tryb obiektu")
        else:
            print("Tryb kamery")


# obsluga ruchu myszy
def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    # zapisywanie przesuniecia podczas nacisniecia przycisku
    if left_mouse_button_pressed or right_mouse_button_pressed:
        delta_x += x_pos - mouse_x_pos_old
        delta_y += y_pos - mouse_y_pos_old

    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


# obsluga przyciskow myszy
def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed
    global mouse_x_pos_old, mouse_y_pos_old
    global delta_x, delta_y

    # sprawdzenie lewego przycisku myszy
    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            left_mouse_button_pressed = 1
        else:
            left_mouse_button_pressed = 0

    # sprawdzenie prawego przycisku myszy
    if button == GLFW_MOUSE_BUTTON_RIGHT:
        if action == GLFW_PRESS:
            right_mouse_button_pressed = 1
        else:
            right_mouse_button_pressed = 0

    # zapisanie pozycji myszy po nacisnieciu
    if action == GLFW_PRESS:
        mouse_x_pos_old, mouse_y_pos_old = glfwGetCursorPos(window)
        delta_x = 0.0
        delta_y = 0.0


# glowna funkcja programu
def main():
    global task, last_time

    # wybor zadania
    task = choose_task()

    # inicjalizacja biblioteki glfw
    if not glfwInit():
        sys.exit(-1)

    # tworzenie okna
    window = glfwCreateWindow(
        800, 600,
        "Laboratorium 4 - zadanie " + str(task),
        None, None
    )

    # sprawdzenie poprawnosci utworzenia okna
    if not window:
        glfwTerminate()
        sys.exit(-1)

    # ustawienie aktywnego okna
    glfwMakeContextCurrent(window)

    # rejestracja funkcji obslugujacych zdarzenia
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)

    # wlaczenie synchronizacji klatek
    glfwSwapInterval(1)

    # ustawienia poczatkowe
    startup()

    width, height = glfwGetFramebufferSize(window)
    update_viewport(window, width, height)

    # zapis czasu poczatkowego
    last_time = glfwGetTime()

    # wyswietlenie instrukcji sterowania
    print("\nSterowanie:")
    print("LPM + mysz - obrot")

    if task in (2, 4):
        print("PPM + ruch pionowy - skalowanie")

    if task in (3, 4):
        print("PPM + ruch pionowy - zmiana odleglosci kamery")

    if task == 4:
        print("C - zmiana trybu kamera/obiekt")

    if task == 5:
        print("W/S - przod i tyl")
        print("A/D - lewo i prawo")
        print("LPM + mysz - kierunek patrzenia")

    print("ESC - wyjscie")

    # glowna petla programu
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), window)

        glfwSwapBuffers(window)
        glfwPollEvents()

    # zakonczenie programu
    shutdown()
    glfwTerminate()


# uruchomienie programu
if __name__ == '__main__':
    main()