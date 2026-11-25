import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
# scale = 1.0
R = 10.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

cam_pos = [0.0, 0.0, 10.0]
theta = -90.0
phi = 0.0
keys = {}


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
    global theta
    global phi
    global scale
    global R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # gluLookAt(viewer[0], viewer[1], viewer[2],
    #           0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # if left_mouse_button_pressed:
    #     theta += delta_x * pix2angle
    #     phi += delta_y * pix2angle

# Prawy przycisk - obrót modelu
    # if right_mouse_button_pressed:
    #     scale += delta_x * 0.01
    #     if scale < 0.1:
    #         scale = 0.1

# Prawy przycisk - obrót kamerą
    # if right_mouse_button_pressed:
    #     R += delta_x * 0.05
    #     if R < 2.0:
    #         R = 2.0
    #     elif R > 30.0:
    #         R = 30.0
    #
    # theta_rad = math.radians(theta)
    # phi_rad = math.radians(phi)
    #
    # x_eye = R * math.cos(theta_rad) * math.cos(phi_rad)
    # y_eye = R * math.sin(phi_rad)
    # z_eye = R * math.sin(theta_rad) * math.cos(phi_rad)
    #
    # phi %= 360.0
    # theta %= 360.0
    #
    # if 90.0 < phi < 270.0:
    #     up_y = -1.0
    # else:
    #     up_y = 1.0
    #
    # gluLookAt(x_eye, y_eye, z_eye, 0.0, 0.0, 0.0, 0.0, up_y, 0.0)

    # glRotatef(theta, 0.0, 1.0, 0.0)
    # glRotatef(phi, 1.0, 0.0, 1.0)
    # glScalef(scale, scale, scale)

# Zadanie na 5
    first_person_move()

    axes()
    example_object()

    glFlush()


def first_person_move():
    global theta, phi, delta_x, delta_y

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi -= delta_y * pix2angle
        phi = max(-89.0, min(89.0, phi))

    front_x = math.cos(math.radians(theta)) * math.cos(math.radians(phi))
    front_y = math.sin(math.radians(phi))
    front_z = math.sin(math.radians(theta)) * math.cos(math.radians(phi))

    right_len = math.hypot(-front_z, front_x)
    right_x = -front_z / right_len if right_len > 0 else 1.0
    right_z = front_x / right_len if right_len > 0 else 0.0

    speed = 0.15
    if keys.get(GLFW_KEY_W):
        cam_pos[0] += front_x * speed
        cam_pos[1] += front_y * speed
        cam_pos[2] += front_z * speed
    if keys.get(GLFW_KEY_S):
        cam_pos[0] -= front_x * speed
        cam_pos[1] -= front_y * speed
        cam_pos[2] -= front_z * speed
    if keys.get(GLFW_KEY_A):
        cam_pos[0] -= right_x * speed
        cam_pos[2] -= right_z * speed
    if keys.get(GLFW_KEY_D):
        cam_pos[0] += right_x * speed
        cam_pos[2] += right_z * speed

    gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
              cam_pos[0] + front_x, cam_pos[1] + front_y, cam_pos[2] + front_z,
              0.0, 1.0, 0.0)

    delta_x = 0
    delta_y = 0

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
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if action == GLFW_PRESS:
        keys[key] = True
    elif action == GLFW_RELEASE:
        keys[key] = False


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
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