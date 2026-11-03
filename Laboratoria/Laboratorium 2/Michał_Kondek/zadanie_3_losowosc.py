import random
import glfw
from OpenGL.GL import *

SEED = 17
DEFORMACJA = 0.77
LOSOWE_KOLORY = True
TYTUL = 'zad. 3 - losowe kolory i deformacja na 4'

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

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    random.seed(SEED)
    prostokat(-45.0, -25.0, 90.0, 50.0, DEFORMACJA)

def ustaw_rzutnie(window, width, height):
    bok = min(width, height)
    glViewport((width - bok) // 2, (height - bok) // 2, bok, bok)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-100.0, 100.0, -100.0, 100.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def klawisz(window, key, scancode, action, mods):
    global SEED, DEFORMACJA, LOSOWE_KOLORY
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_R:
        SEED += 1
    elif key == glfw.KEY_UP:
        DEFORMACJA = min(0.9, round(DEFORMACJA + 0.05, 2))
    elif key == glfw.KEY_DOWN:
        DEFORMACJA = max(0.0, round(DEFORMACJA - 0.05, 2))
    elif key == glfw.KEY_C:
        LOSOWE_KOLORY = not LOSOWE_KOLORY

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
