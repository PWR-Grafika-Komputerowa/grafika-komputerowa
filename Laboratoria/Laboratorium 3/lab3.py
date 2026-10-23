import math
import random

import glfw
from OpenGL.GL import *

N = 40
MODE = "strip"

ANGLE_RANGE = 2 * math.pi

def create_egg():
    vertices = []

    for i in range(N):
        u = i / (N - 1)
        row = []

        for j in range(N):
            v = j / (N - 1)

            r = (
                -90 * u**5
                + 225 * u**4
                - 270 * u**3
                + 180 * u**2
                - 45 * u
            )

            x = r * math.cos(ANGLE_RANGE * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = r * math.sin(ANGLE_RANGE * v)

            row.append((x, y, z))

        vertices.append(row)

    return vertices

def create_colors():
    random.seed(10)
    colors = []

    for i in range(N):
        row = []

        for j in range(N):
            color = (
                random.uniform(0.2, 1.0),
                random.uniform(0.2, 1.0),
                random.uniform(0.2, 1.0)
            )
            row.append(color)

        colors.append(row)

    return colors


vertices = create_egg()
colors = create_colors()

def axes():
    glLineWidth(2.0)
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5, 0, 0)
    glVertex3f(5, 0, 0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0, -5, 0)
    glVertex3f(0, 5, 0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0, 0, -5)
    glVertex3f(0, 0, 5)

    glEnd()

def draw_points():
    glPointSize(4.0)
    glBegin(GL_POINTS)

    for i in range(N):
        for j in range(N):
            glColor3f(1.0, 1.0, 0.0)
            glVertex3f(*vertices[i][j])

    glEnd()

def draw_lines():
    glLineWidth(1.0)
    glBegin(GL_LINES)

    for i in range(N):
        for j in range(N):

            if i + 1 < N:
                glColor3f(0.2, 0.8, 1.0)
                glVertex3f(*vertices[i][j])
                glVertex3f(*vertices[i + 1][j])

            if j + 1 < N:
                glColor3f(0.2, 0.8, 1.0)
                glVertex3f(*vertices[i][j])
                glVertex3f(*vertices[i][j + 1])

    glEnd()

def draw_triangles():
    glBegin(GL_TRIANGLES)

    for i in range(N - 1):
        for j in range(N - 1):

            p00 = vertices[i][j]
            p10 = vertices[i + 1][j]
            p01 = vertices[i][j + 1]
            p11 = vertices[i + 1][j + 1]

            c00 = colors[i][j]
            c10 = colors[i + 1][j]
            c01 = colors[i][j + 1]
            c11 = colors[i + 1][j + 1]

            glColor3f(*c00)
            glVertex3f(*p00)

            glColor3f(*c10)
            glVertex3f(*p10)

            glColor3f(*c01)
            glVertex3f(*p01)

            glColor3f(*c10)
            glVertex3f(*p10)

            glColor3f(*c11)
            glVertex3f(*p11)

            glColor3f(*c01)
            glVertex3f(*p01)

    glEnd()

def draw_strip():
    for i in range(N - 1):

        glBegin(GL_TRIANGLE_STRIP)

        for j in range(N):

            glColor3f(*colors[i][j])
            glVertex3f(*vertices[i][j])

            glColor3f(*colors[i + 1][j])
            glVertex3f(*vertices[i + 1][j])

        glEnd()

def startup():
    glClearColor(0.08, 0.08, 0.12, 1.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(
        -7.5, 7.5,
        -7.5, 7.5,
        -20.0, 20.0
    )

    glMatrixMode(GL_MODELVIEW)

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    axes()

    glLoadIdentity()

    time = glfw.get_time()
    angle = time * 180.0 / math.pi

    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

    if MODE == "points":
        draw_points()

    elif MODE == "lines":
        draw_lines()

    elif MODE == "triangles":
        draw_triangles()

    elif MODE == "strip":
        draw_strip()

def main():
    if not glfw.init():
        raise RuntimeError("Nie mozna uruchomic GLFW!")

    window = glfw.create_window(
        800, 800,
        "Model jajka 3D",
        None, None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Nie mozna utworzyc okna!")

    glfw.make_context_current(window)

    glfw.swap_interval(1)

    startup()

    while not glfw.window_should_close(window):
        render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
