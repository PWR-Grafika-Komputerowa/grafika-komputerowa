
import glfw
from OpenGL.GL import *

if not glfw.init():
    raise RuntimeError("Nie udało się uruchomić GLFW")

window = glfw.create_window(800, 600, "Laboratorium 2", None, None)

if not window:
    glfw.terminate()
    raise RuntimeError("Nie udało się utworzyć okna")

glfw.make_context_current(window)

# Ustawienie układu współrzędnych

def ustaw_widok(window, width, height):
    if width == 0 or height == 0:
        return

    # Obszar renderowania
    glViewport(0, 0, width, height)

    # Proporcje okna
    ar = width / height

    # Macierz projekcji
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if ar >= 1:
        glOrtho(-100 * ar, 100 * ar,
                -100, 100, -1, 1)
    else:
        glOrtho(-100, 100,
                -100 / ar, 100 / ar, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# Aktualizacja widoku po zmianie rozmiaru okna
glfw.set_framebuffer_size_callback(window, ustaw_widok)

width, height = glfw.get_framebuffer_size(window)
ustaw_widok(window, width, height)


# Płynna interpolacja kolorów
glShadeModel(GL_SMOOTH)

while not glfw.window_should_close(window):
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)

    # Górny wierzchołek - czerwony
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 80.0)

    # Lewy dolny wierzchołek - zielony
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-80.0, -60.0)

    # Prawy dolny wierzchołek - niebieski
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(80.0, -60.0)

    glEnd()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
