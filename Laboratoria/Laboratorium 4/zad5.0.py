import sys
from math import sin, cos, radians, pi
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

theta = 90.0
phi = 20.0
scale = 1.0
R = 25.0
pix2angle = 1.0
left_mouse_button_pressed = right_mouse_button_pressed = False
mouse_x_pos_old = mouse_y_pos_old = 0.0
delta_x = delta_y = 0.0
camera_mode = True
angles = [0.0] * 7
selected = 1
count = 8


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
    if button == GLFW_MOUSE_BUTTON_RIGHT:
        right_mouse_button_pressed = action == GLFW_PRESS
    mouse_x_pos_old, mouse_y_pos_old = glfwGetCursorPos(window)
    delta_x = delta_y = 0.0


def mouse_motion_callback(window, x, y):
    global mouse_x_pos_old, mouse_y_pos_old, delta_x, delta_y
    if left_mouse_button_pressed or right_mouse_button_pressed:
        delta_x += x - mouse_x_pos_old
        delta_y += y - mouse_y_pos_old
    mouse_x_pos_old, mouse_y_pos_old = x, y


def keyboard_key_callback(window, key, scancode, action, mods):
    global camera_mode, theta, phi, R, scale, selected
    if action == GLFW_PRESS:
        if key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, True)
        if key == GLFW_KEY_LEFT:
            selected = max(1, selected - 1)
        if key == GLFW_KEY_RIGHT:
            selected = min(count - 1, selected + 1)
        if key == GLFW_KEY_R:
            angles[:] = [0.0] * (count - 1)
            theta, phi, R = 90.0, 20.0, 25.0
    if action in (GLFW_PRESS, GLFW_REPEAT):
        if key == GLFW_KEY_UP:
            angles[selected-1] = min(45.0, angles[selected-1] + 5.0)
        if key == GLFW_KEY_DOWN:
            angles[selected-1] = max(-45.0, angles[selected-1] - 5.0)
    glfwSetWindowTitle(window, f'4.3 - przegub {selected}/{count-1} | strzalki, R, mysz')


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



def torus():
    # R - promien glowny, r - promien przekroju rurki.
    major, minor = 1.0, 0.23
    for i in range(36):
        glBegin(GL_QUAD_STRIP)
        for j in range(17):
            v = 2*pi*j/16
            for k in (i, i+1):
                u = 2*pi*k/36
                glNormal3f(cos(u)*cos(v), sin(u)*cos(v), sin(v))
                glVertex3f((major+minor*cos(v))*cos(u),
                           (major+minor*cos(v))*sin(u), minor*sin(v))
        glEnd()


def example_object():
    glPushMatrix()
    glTranslatef(-1.65*(count-1)/2, 0, 0)
    glEnable(GL_LIGHTING)
    for i in range(count):
        if i > 0:
            # obrot w polowie odleglosci miedzy ogniwami.
            glTranslatef(0.825, 0, 0)
            glRotatef(angles[i-1], 0, 0, 1)
            glTranslatef(0.825, 0, 0)
        glPushMatrix()
        glRotatef(90*(i % 2), 1, 0, 0)
        if i == selected:
            glColor3f(1.0, 0.65, 0.12)
        else:
            glColor3f(0.35, 0.65, 0.85)
        torus()
        glPopMatrix()
    glDisable(GL_LIGHTING)
    glPopMatrix()


def render(time):
    global theta, phi, R, delta_x, delta_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    if left_mouse_button_pressed:
        theta = (theta + delta_x * pix2angle) % 360
        phi = (phi + delta_y * pix2angle) % 360
    if right_mouse_button_pressed:
        R = min(65.0, max(3.0, R + delta_y * 0.08))
    a, b = radians(theta), radians(phi)
    eye = (R*cos(a)*cos(b), R*sin(b), R*sin(a)*cos(b))
    up = (-cos(a)*sin(b), cos(b), -sin(a)*sin(b))
    gluLookAt(*eye, 0, 0, 0, *up)
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 10, 15, 1))
    delta_x = delta_y = 0.0
    axes()
    example_object()
    glFlush()


def startup():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1))
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.25, 0.25, 0.25, 1))


def shutdown():
    pass


def main():
    global mouse_x_pos_old, mouse_y_pos_old
    if not glfwInit():
        sys.exit('nie udalo sie uruchomic GLFW')
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 2)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1)
    window = glfwCreateWindow(400, 400, '5.0 - lancuch torusow | strzalki, R, mysz', None, None)
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
