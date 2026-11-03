import random
import glfw
from OpenGL.GL import *

SEED = 1
POZIOM = 1
DEFORMACJA = 0.0
LOSOWE_KOLORY = True
TYTUL = '4 — prostokątny dywan Sierpińskiego na 4.5'

def prostokat(x, y, a, b, d=0.0):
    szer = a * random.uniform(1 - d, 1 + d)
    wys = b * random.uniform(1 - d, 1 + d)
    punkty = [(x, y), (x + szer, y), (x + szer, y + wys), (x, y + wys)]
    kolory = [(random.random(), random.random(), random.random()) for _ in range(4)]
    glBegin(GL_TRIANGLES)
    for i in (0, 1, 2, 0, 2, 3):
        glColor3f(*(kolory[i] if LOSOWE_KOLORY else (0.65, 0.22, 0.05)))
        glVertex2f(*punkty[i])
    glEnd()

def dywan(x, y, a, b, poziom):
    if poziom == 0:
        prostokat(x, y, a, b, DEFORMACJA)
        return
    for wiersz in range(3):
        for kolumna in range(3):
            if wiersz == 1 and kolumna == 1:    # Co 3 daje srodek pusty
                continue
            dywan(x + kolumna * a / 3, y + wiersz * b / 3, a / 3, b / 3, poziom - 1)    # Dywan w nowym rozmiarze i przesuniety

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    random.seed(SEED)
    dywan(-90.0, -65.0, 180.0, 130.0, POZIOM)

def ustaw_rzutnie(window, width, height):
    bok = min(width, height)
    glViewport((width - bok) // 2, (height - bok) // 2, bok, bok)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-100.0, 100.0, -100.0, 100.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def klawisz(window, key, scancode, action, mods):
    global SEED, POZIOM, DEFORMACJA, LOSOWE_KOLORY
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_R:
        SEED += 1
    elif key == glfw.KEY_N:
        POZIOM = min(5, POZIOM + 1)
    elif key == glfw.KEY_B:
        POZIOM = max(0, POZIOM - 1)
    elif key == glfw.KEY_C:
        LOSOWE_KOLORY = not LOSOWE_KOLORY
    elif key == glfw.KEY_D:
        DEFORMACJA = 0.06 if DEFORMACJA == 0.0 else 0.0

glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
window = glfw.create_window(700, 700, TYTUL, None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)
glfw.set_framebuffer_size_callback(window, ustaw_rzutnie)
glfw.set_key_callback(window, klawisz)
glClearColor(1.0, 1.0, 1.0, 1.0)
glShadeModel(GL_SMOOTH)
ustaw_rzutnie(window, *glfw.get_framebuffer_size(window))
while not glfw.window_should_close(window):
    render()
    glfw.swap_buffers(window)
    glfw.wait_events()
glfw.destroy_window(window)
glfw.terminate()
