
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
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
ar = 800 / 600
glOrtho(-100, 100, -100 / ar, 100 / ar, -1, 1)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Płynna interpolacja kolorów
glShadeModel(GL_SMOOTH)

while not glfw.window_should_close(window):
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)


    glBegin(GL_TRIANGLES)
    
    # Pierwszy trójkąt - czerwony
    glColor3f(1.0, 0.2, 0.3)
    glVertex2f(-50.0, -50.0)
    glVertex2f(-50.0, 50.0)
    glVertex2f(50.0, 50.0)
    
    # Drugi trójkąt - zielony
    glColor3f(0.0, 1.0, 0.3)
    glVertex2f(-50.0, -50.0)
    glVertex2f(50.0, 50.0)
    glVertex2f(50.0, -50.0)
    
    glEnd()


    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
