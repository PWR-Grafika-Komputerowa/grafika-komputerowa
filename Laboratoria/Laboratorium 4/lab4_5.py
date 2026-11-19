#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

camera = {
    "pos": [0.0, 0.0, 10.0],
    "yaw": -90.0,
    "pitch": 0.0,
    "speed": 0.1,
    "sensitivity": 0.2
}

mouse = {
    "lmb_down": False,
    "last_x": 0.0,
    "last_y": 0.0
}

active_keys = {
    GLFW_KEY_W: False,
    GLFW_KEY_S: False,
    GLFW_KEY_A: False,
    GLFW_KEY_D: False
}


def init_scene():
    on_resize(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def draw_axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def draw_model():
    glColor3f(1.0, 1.0, 1.0)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glRotatef(-90.0, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glPopMatrix()

    for angle in (90.0, -90.0):
        glPushMatrix()
        glRotatef(angle, 1.0, 0.0, 1.0)
        glTranslatef(0.0, 0.0, 1.5)
        gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
        glPopMatrix()

    glPopMatrix()
    gluDeleteQuadric(quadric)


def update_camera_position():
    yaw_rad = math.radians(camera["yaw"])
    pitch_rad = math.radians(camera["pitch"])

    dir_x = math.cos(yaw_rad) * math.cos(pitch_rad)
    dir_y = math.sin(pitch_rad)
    dir_z = math.sin(yaw_rad) * math.cos(pitch_rad)

    side_x = math.cos(yaw_rad + math.pi / 2.0)
    side_z = math.sin(yaw_rad + math.pi / 2.0)

    step = camera["speed"]
    pos = camera["pos"]

    if active_keys[GLFW_KEY_W]:
        pos[0] += dir_x * step
        pos[1] += dir_y * step
        pos[2] += dir_z * step
    if active_keys[GLFW_KEY_S]:
        pos[0] -= dir_x * step
        pos[1] -= dir_y * step
        pos[2] -= dir_z * step
    if active_keys[GLFW_KEY_A]:
        pos[0] -= side_x * step
        pos[2] -= side_z * step
    if active_keys[GLFW_KEY_D]:
        pos[0] += side_x * step
        pos[2] += side_z * step

    return dir_x, dir_y, dir_z


def render_frame():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    dir_x, dir_y, dir_z = update_camera_position()
    px, py, pz = camera["pos"]

    gluLookAt(
        px, py, pz,
        px + dir_x, py + dir_y, pz + dir_z,
        0.0, 1.0, 0.0
    )

    draw_axes()
    draw_model()
    glFlush()


def on_resize(window, width, height):
    width = max(width, 1)
    height = max(height, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, (height - width) // 2, width, width)
    else:
        glViewport((width - height) // 2, 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def on_key(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key in active_keys:
        if action == GLFW_PRESS:
            active_keys[key] = True
        elif action == GLFW_RELEASE:
            active_keys[key] = False


def on_mouse_move(window, x_pos, y_pos):
    dx = x_pos - mouse["last_x"]
    dy = y_pos - mouse["last_y"]
    mouse["last_x"] = x_pos
    mouse["last_y"] = y_pos

    if mouse["lmb_down"]:
        camera["yaw"] += dx * camera["sensitivity"]
        camera["pitch"] -= dy * camera["sensitivity"]
        camera["pitch"] = max(-89.0, min(89.0, camera["pitch"]))


def on_mouse_button(window, button, action, mods):
    if button == GLFW_MOUSE_BUTTON_LEFT:
        mouse["lmb_down"] = (action == GLFW_PRESS)


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, on_resize)
    glfwSetKeyCallback(window, on_key)
    glfwSetCursorPosCallback(window, on_mouse_move)
    glfwSetMouseButtonCallback(window, on_mouse_button)
    glfwSwapInterval(1)

    init_scene()
    while not glfwWindowShouldClose(window):
        render_frame()
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == '__main__':
    main()