import glfw
from OpenGL.GL import *

TYTUL = '1 - trójkąt RGB na 3'

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-70.0, -60.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(70.0, -60.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 70.0)
    glEnd()

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
