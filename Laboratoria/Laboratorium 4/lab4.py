#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

ZAD = 1

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

scale = 1.0
R = 10.0

# Flaga trybu dla zadania 4 (True = ruch kamery, False = obrót/skalowanie obiektu)
camera_mode = True

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0


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


def render(time):
    global theta, phi, scale, R, viewer, delta_x, delta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if ZAD == 1:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle

        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)

    elif ZAD == 2:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle

        if right_mouse_button_pressed:
            scale += delta_y * 0.01

        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
        glScalef(scale, scale, scale)

    elif ZAD == 3:
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle

        if right_mouse_button_pressed:
            R += delta_y * 0.05

        theta_rad = theta * math.pi / 180.0
        phi_rad = phi * math.pi / 180.0

        x_eye = R * math.cos(theta_rad) * math.cos(phi_rad)
        y_eye = R * math.sin(phi_rad)
        z_eye = R * math.sin(theta_rad) * math.cos(phi_rad)

        gluLookAt(x_eye, y_eye, z_eye,
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    elif ZAD == 4:
        if camera_mode:
            if left_mouse_button_pressed:
                theta = (theta + delta_x * pix2angle) % 360.0
                phi = (phi + delta_y * pix2angle) % 360.0

            if right_mouse_button_pressed:
                R += delta_y * 0.05
                # Ograniczenie zakresu przybliżania/oddalania kamery
                R = max(2.0, min(50.0, R))

            theta_rad = theta * math.pi / 180.0
            phi_rad = phi * math.pi / 180.0

            x_eye = R * math.cos(theta_rad) * math.cos(phi_rad)
            y_eye = R * math.sin(phi_rad)
            z_eye = R * math.sin(theta_rad) * math.cos(phi_rad)

            if 90.0 < phi < 270.0:
                up_y = -1.0
            else:
                up_y = 1.0

            gluLookAt(x_eye, y_eye, z_eye,
                      0.0, 0.0, 0.0, 0.0, up_y, 0.0)
        else:
            # Tryb obracania i skalowania obiektu
            gluLookAt(viewer[0], viewer[1], viewer[2],
                      0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

            if left_mouse_button_pressed:
                theta = (theta + delta_x * pix2angle) % 360.0
                phi = (phi + delta_y * pix2angle) % 360.0

            if right_mouse_button_pressed:
                scale += delta_y * 0.01
                scale = max(0.1, min(5.0, scale))

            glRotatef(theta, 0.0, 1.0, 0.0)
            glRotatef(phi, 1.0, 0.0, 0.0)
            glScalef(scale, scale, scale)

    elif ZAD == 5:
        if left_mouse_button_pressed:
            theta = (theta + delta_x * pix2angle) % 360.0
            phi = max(-89.0, min(89.0, phi - delta_y * pix2angle))

        theta_rad = theta * math.pi / 180.0
        phi_rad = phi * math.pi / 180.0

        # Wektor kierunku patrzenia kamery (forward)
        dir_x = math.sin(theta_rad) * math.cos(phi_rad)
        dir_y = math.sin(phi_rad)
        dir_z = -math.cos(theta_rad) * math.cos(phi_rad)

        # Punkt zainteresowania = położenie obserwatora + wektor kierunku patrzenia
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  viewer[0] + dir_x, viewer[1] + dir_y, viewer[2] + dir_z,
                  0.0, 1.0, 0.0)

    delta_x = 0
    delta_y = 0

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    if width == 0:
        width = 1
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


def reset_view():
    global viewer, theta, phi, scale, R, delta_x, delta_y, camera_mode
    viewer = [0.0, 0.0, 10.0]
    theta = 0.0
    phi = 0.0
    scale = 1.0
    R = 10.0
    delta_x = 0
    delta_y = 0
    camera_mode = True


def keyboard_key_callback(window, key, scancode, action, mods):
    global camera_mode, ZAD, viewer

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    # Przełączanie trybu kamera
    if (key == GLFW_KEY_C or key == GLFW_KEY_SPACE) and action == GLFW_PRESS:
        camera_mode = not camera_mode

    # Reset widoku w dowolnym momencie klawiszem R
    if key == GLFW_KEY_R and action == GLFW_PRESS:
        reset_view()

    if action == GLFW_PRESS:
        if key == GLFW_KEY_1:
            ZAD = 1
            reset_view()
        elif key == GLFW_KEY_2:
            ZAD = 2
            reset_view()
        elif key == GLFW_KEY_3:
            ZAD = 3
            reset_view()
        elif key == GLFW_KEY_4:
            ZAD = 4
            reset_view()
        elif key == GLFW_KEY_5:
            ZAD = 5
            reset_view()

    # Obsługa klawiszy [W][S][A][D] dla kamery pierwszoosobowej
    if ZAD == 5 and action in (GLFW_PRESS, GLFW_REPEAT):
        speed = 0.4
        theta_rad = theta * math.pi / 180.0
        phi_rad = phi * math.pi / 180.0

        # Wektor do przodu (forward)
        forward_x = math.sin(theta_rad) * math.cos(phi_rad)
        forward_y = math.sin(phi_rad)
        forward_z = -math.cos(theta_rad) * math.cos(phi_rad)

        # Wektor w prawo (right = forward x up)
        right_x = math.cos(theta_rad)
        right_z = math.sin(theta_rad)

        if key == GLFW_KEY_W:
            viewer[0] += forward_x * speed
            viewer[1] += forward_y * speed
            viewer[2] += forward_z * speed
        elif key == GLFW_KEY_S:
            viewer[0] -= forward_x * speed
            viewer[1] -= forward_y * speed
            viewer[2] -= forward_z * speed
        elif key == GLFW_KEY_D:
            viewer[0] += right_x * speed
            viewer[2] += right_z * speed
        elif key == GLFW_KEY_A:
            viewer[0] -= right_x * speed
            viewer[2] -= right_z * speed


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, mouse_x_pos_old
    global delta_y, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            left_mouse_button_pressed = 1
        else:
            left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT:
        if action == GLFW_PRESS:
            right_mouse_button_pressed = 1
        else:
            right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
