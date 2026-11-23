#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


MODE_OBJECT = 0
MODE_ORBIT = 1
MODE_FPS = 2
MODE_NAMES = {
    MODE_OBJECT: "1: Obrot i skalowanie obiektu",
    MODE_ORBIT: "2: Kamera orbitalna wokol modelu",
    MODE_FPS: "3: Kamera pierwszoosobowa (FPS)",
}

current_mode = MODE_OBJECT
window_ref = None

viewer = [0.0, 0.0, 10.0]

#parametry obrotu i skali obiektu (zad. 3.0 i 3.5)
theta = 0.0
phi = 0.0
scale = 1.0

#parametry kamery orbitalnej (zad. 4.0 i 4.5)
orbit_theta = 90.0
orbit_phi = 0.0
orbit_R = 10.0

#parametry kamery pierwszoosobowej FPS (zad. 5.0)
fps_pos = [0.0, 0.0, 10.0]
fps_yaw = -90.0
fps_pitch = 0.0
fps_speed = 5.0

pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0.0
mouse_y_pos_old = 0.0
delta_x = 0.0
delta_y = 0.0

keys_pressed = set()
last_frame_time = 0.0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def set_mode(new_mode):
    global current_mode
    current_mode = new_mode
    title = f"Lab 4 - {MODE_NAMES[current_mode]}"
    if window_ref is not None:
        glfwSetWindowTitle(window_ref, title)
    print(f"Aktywny tryb -> {MODE_NAMES[current_mode]}")


def reset_current_mode():
    global theta, phi, scale
    global orbit_theta, orbit_phi, orbit_R
    global fps_pos, fps_yaw, fps_pitch

    if current_mode == MODE_OBJECT:
        theta = 0.0
        phi = 0.0
        scale = 1.0
    elif current_mode == MODE_ORBIT:
        orbit_theta = 90.0
        orbit_phi = 0.0
        orbit_R = 10.0
    elif current_mode == MODE_FPS:
        fps_pos = [0.0, 0.0, 10.0]
        fps_yaw = -90.0
        fps_pitch = 0.0


def _render_object_mode():
    global theta, phi, scale

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        scale += delta_y * 0.01
        scale = max(0.1, min(5.0, scale))

    glRotatef(phi, 1.0, 0.0, 0.0)
    glRotatef(theta, 0.0, 1.0, 0.0)
    glScalef(scale, scale, scale)


def _render_orbit_mode():
    global orbit_theta, orbit_phi, orbit_R

    if left_mouse_button_pressed:
        orbit_theta = (orbit_theta + delta_x * pix2angle) % 360.0
        orbit_phi = (orbit_phi + delta_y * pix2angle) % 360.0

    if right_mouse_button_pressed:
        orbit_R += delta_y * 0.05
        orbit_R = max(2.0, min(30.0, orbit_R))

    theta_rad = math.radians(orbit_theta)
    phi_rad = math.radians(orbit_phi)

    cos_phi = math.cos(phi_rad)
    #zabezpieczenie przed osobliwoscia dokladnie na biegunach (cos(phi) == 0)
    if abs(cos_phi) < 1e-4:
        cos_phi = 1e-4 if cos_phi >= 0 else -1e-4

    x_eye = orbit_R * math.cos(theta_rad) * cos_phi
    y_eye = orbit_R * math.sin(phi_rad)
    z_eye = orbit_R * math.sin(theta_rad) * cos_phi
    up_y = 1.0 if cos_phi > 0 else -1.0

    gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0, 0.0, up_y, 0.0)


def _render_fps_mode(dt):
    global fps_yaw, fps_pitch

    if left_mouse_button_pressed:
        fps_yaw = (fps_yaw + delta_x * pix2angle * 0.5) % 360.0
        fps_pitch = max(-89.0, min(89.0, fps_pitch - delta_y * pix2angle * 0.5))

    yaw_rad = math.radians(fps_yaw)
    pitch_rad = math.radians(fps_pitch)

    dir_x = math.cos(yaw_rad) * math.cos(pitch_rad)
    dir_y = math.sin(pitch_rad)
    dir_z = math.sin(yaw_rad) * math.cos(pitch_rad)

    #wektor w prawo (iloczyn wektorowy forward x up(0, 1, 0))
    right_x = -dir_z
    right_z = dir_x
    right_len = math.hypot(right_x, right_z)
    if right_len > 1e-6:
        right_x /= right_len
        right_z /= right_len

    step = fps_speed * dt
    if GLFW_KEY_W in keys_pressed:
        fps_pos[0] += dir_x * step
        fps_pos[1] += dir_y * step
        fps_pos[2] += dir_z * step
    if GLFW_KEY_S in keys_pressed:
        fps_pos[0] -= dir_x * step
        fps_pos[1] -= dir_y * step
        fps_pos[2] -= dir_z * step
    if GLFW_KEY_D in keys_pressed:
        fps_pos[0] += right_x * step
        fps_pos[2] += right_z * step
    if GLFW_KEY_A in keys_pressed:
        fps_pos[0] -= right_x * step
        fps_pos[2] -= right_z * step

    gluLookAt(fps_pos[0], fps_pos[1], fps_pos[2],
              fps_pos[0] + dir_x, fps_pos[1] + dir_y, fps_pos[2] + dir_z,
              0.0, 1.0, 0.0)


def render(time):
    global delta_x, delta_y, last_frame_time

    dt = time - last_frame_time if last_frame_time > 0.0 else 0.0
    last_frame_time = time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if current_mode == MODE_OBJECT:
        _render_object_mode()
    elif current_mode == MODE_ORBIT:
        _render_orbit_mode()
    elif current_mode == MODE_FPS:
        _render_fps_mode(dt)

    delta_x = 0.0
    delta_y = 0.0

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if action == GLFW_PRESS:
        keys_pressed.add(key)
        if key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)
        elif key == GLFW_KEY_1:
            set_mode(MODE_OBJECT)
        elif key == GLFW_KEY_2:
            set_mode(MODE_ORBIT)
        elif key == GLFW_KEY_3:
            set_mode(MODE_FPS)
        elif key == GLFW_KEY_M:
            set_mode((current_mode + 1) % 3)
        elif key == GLFW_KEY_R:
            reset_current_mode()
    elif action == GLFW_RELEASE:
        keys_pressed.discard(key)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x += x_pos - mouse_x_pos_old
    delta_y += y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT:
        left_mouse_button_pressed = 1 if action == GLFW_PRESS else 0
    elif button == GLFW_MOUSE_BUTTON_RIGHT:
        right_mouse_button_pressed = 1 if action == GLFW_PRESS else 0


def main():
    global window_ref

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(600, 600, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    window_ref = window
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    print("Sterowanie:")
    print("  [1] Tryb obiektu (LPM: obrot X/Y, PPM: skalowanie)")
    print("  [2] Tryb kamery orbitalnej (LPM: obrot wokol modelu, PPM: przyblizenie/oddalenie)")
    print("  [3] Tryb kamery FPS (LPM + mysz: rozgladanie, W/S/A/D: ruch)")
    print("  [M] Przelacz tryb cyklicznie | [R] Resetuj biezacy tryb | [ESC] Wyjscie")
    set_mode(MODE_OBJECT)

    startup()
    update_viewport(window, 600, 600)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
