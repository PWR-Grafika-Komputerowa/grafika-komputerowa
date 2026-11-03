import math
import glfw
from OpenGL.GL import *

POZIOM = 3
WYPELNIENIE = True
TYTUL = '5 — płatek Kocha na 5.0'

def odcinek_kocha(a, b, poziom, brzeg, trojkaty):   # a i b to konce odcinka
    if poziom == 0:
        brzeg.append(a)
        return
    dx = (b[0] - a[0]) / 3  # przesuniecie o 1/3 odcinka
    dy = (b[1] - a[1]) / 3
    p = (a[0] + dx, a[1] + dy)  # p w 1/3
    q = (a[0] + 2 * dx, a[1] + 2 * dy)  # q w 2/3
    r = (p[0] + dx / 2 + dy * math.sqrt(3) / 2, p[1] - dx * math.sqrt(3) / 2 + dy / 2)  # szczyt nowego trojkata
    trojkaty.append((p, r, q))
    odcinek_kocha(a, p, poziom - 1, brzeg, trojkaty)
    odcinek_kocha(p, r, poziom - 1, brzeg, trojkaty)
    odcinek_kocha(r, q, poziom - 1, brzeg, trojkaty)
    odcinek_kocha(q, b, poziom - 1, brzeg, trojkaty)

def platek_kocha(poziom):
    a = (-65, -37.5)
    b = (65, -37.5)
    c = (0, -37.5 + 65 * math.sqrt(3))
    brzeg = []
    trojkaty = [(a, b, c)]
    odcinek_kocha(a, b, poziom, brzeg, trojkaty)
    odcinek_kocha(b, c, poziom, brzeg, trojkaty)    # odcinek_kocha dla każdego z 3 bokow
    odcinek_kocha(c, a, poziom, brzeg, trojkaty)
    return (brzeg, trojkaty)

def kolor(punkt):
    x, y = punkt
    glColor3f(0.5 + x / 200, 0.5 + y / 200, 0.5 - (x + y) / 400)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    brzeg, trojkaty = platek_kocha(POZIOM)
    if WYPELNIENIE:
        glBegin(GL_TRIANGLES)
        for trojkat in trojkaty:
            for punkt in trojkat:
                kolor(punkt)
                glVertex2f(*punkt)
        glEnd()
    glColor3f(0.12, 0.12, 0.2)
    glBegin(GL_LINE_LOOP)
    for punkt in brzeg:
        glVertex2f(*punkt)
    glEnd()

def ustaw_rzutnie(window, width, height):
    bok = min(width, height)
    glViewport((width - bok) // 2, (height - bok) // 2, bok, bok)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-100.0, 100.0, -100.0, 100.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def klawisz(window, key, scancode, action, mods):
    global POZIOM, WYPELNIENIE
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_N:
        POZIOM = min(6, POZIOM + 1)
    elif key == glfw.KEY_B:
        POZIOM = max(0, POZIOM - 1)
    elif key == glfw.KEY_F:
        WYPELNIENIE = not WYPELNIENIE

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
