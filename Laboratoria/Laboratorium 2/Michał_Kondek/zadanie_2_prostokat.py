import glfw
from OpenGL.GL import *

TYTUL = '2 - prostokąt z dwóch trójkątów na 3.5'

def prostokat(x, y, a, b):
    glColor3f(0.7, 0.21, 0.12)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)
    glEnd()

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    prostokat(-65.0, -35.0, 130.0, 70.0)

def ustaw_rzutnie(window, width, height):
    bok = min(width, height)
    glViewport((width - bok) // 2, (height - bok) // 2, bok, bok)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-100.0, 100.0, -100.0, 100.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
window = glfw.create_window(700, 700, TYTUL, None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)
glfw.set_framebuffer_size_callback(window, ustaw_rzutnie)
glClearColor(1.0, 1.0, 1.0, 1.0)
glShadeModel(GL_SMOOTH)
ustaw_rzutnie(window, *glfw.get_framebuffer_size(window))
while not glfw.window_should_close(window):
    render()
    glfw.swap_buffers(window)
    glfw.wait_events()
glfw.destroy_window(window)
glfw.terminate()
