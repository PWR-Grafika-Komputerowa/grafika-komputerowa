import sys
from math import sin, cos, radians, pi
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]
theta = phi = 0.0
scale = 1.0
R = 10.0
pix2angle = 1.0
left_mouse_button_pressed = right_mouse_button_pressed = False
mouse_x_pos_old = mouse_y_pos_old = 0.0
delta_x = delta_y = 0.0
camera_mode = True


def update_viewport(window, width, height):
    global pix2angle
    width, height = max(1, width), max(1, height)
    pix2angle = 360.0 / max(1, glfwGetWindowSize(window)[0])
    side = min(width, height)
    glViewport((width - side) // 2, (height - side) // 2, side, side)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, 1.0, 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed, mouse_x_pos_old, mouse_y_pos_old, delta_x, delta_y
    if button == GLFW_MOUSE_BUTTON_LEFT:
        left_mouse_button_pressed = action == GLFW_PRESS
    mouse_x_pos_old, mouse_y_pos_old = glfwGetCursorPos(window)
    delta_x = delta_y = 0.0


def mouse_motion_callback(window, x, y):
    global mouse_x_pos_old, mouse_y_pos_old, delta_x, delta_y
    if left_mouse_button_pressed or right_mouse_button_pressed:
        delta_x += x - mouse_x_pos_old
        delta_y += y - mouse_y_pos_old
    mouse_x_pos_old, mouse_y_pos_old = x, y


def keyboard_key_callback(window, key, scancode, action, mods):
    global camera_mode, theta, phi, R, scale
    if action == GLFW_PRESS:
        if key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, True)



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
    global theta, phi, scale, R, delta_x, delta_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    gluLookAt(*viewer, 0, 0, 0, 0, 1, 0)
    glRotatef(theta, 0, 1, 0)
    glRotatef(phi, 1, 0, 0)
    delta_x = delta_y = 0.0
    axes()
    example_object()
    glFlush()


def startup():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def main():
    global mouse_x_pos_old, mouse_y_pos_old
    if not glfwInit():
        sys.exit('nie udalo sie uruchomic GLFW')
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 2)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1)
    window = glfwCreateWindow(400, 400, '3.0 - obrot X i Y', None, None)
    if not window:
        glfwTerminate()
        sys.exit('nie udalo sie utworzyc okna')
    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetKeyCallback(window, keyboard_key_callback)
    mouse_x_pos_old, mouse_y_pos_old = glfwGetCursorPos(window)
    update_viewport(window, *glfwGetFramebufferSize(window))
    startup()
    while not glfwWindowShouldClose(window):
        glfwPollEvents()
        render(glfwGetTime())
        glfwSwapBuffers(window)
    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()
