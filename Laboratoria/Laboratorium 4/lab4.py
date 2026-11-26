#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]
eye = [0.0, 0.0, 10.0]

theta = -90.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

scale = 1.0

R = 10.0

camera_mode = 2

move_speed = 0.2

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
    global theta, phi, scale, delta_x, delta_y, R, camera_mode

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    if camera_mode == 0: 
    
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle
        
            theta %= 360.0
            phi %= 360.0
        
        if right_mouse_button_pressed:
            R += delta_x * 0.05
        
            if R < 2.0:
                R = 2.0
            if R > 20.0:
                R = 20.0
            
        up_y = 1.0
        
        if phi > 90.0 and phi < 270.0:
            up_y = -1.0
            
        x_eye = R * math.cos(theta * math.pi / 180.0) * math.cos(phi * math.pi / 180.0)
        y_eye = R * math.sin(phi * math.pi / 180.0)
        z_eye = R * math.sin(theta * math.pi / 180.0) * math.cos(phi * math.pi / 180.0)
        
#       gluLookAt(x_eye, y_eye, z_eye,
#             0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0, 0.0, up_y, 0.0)
              
    elif camera_mode == 1: 
        
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle
        
            theta %= 360.0
            phi %= 360.0
    
        if right_mouse_button_pressed:
            scale += delta_x * 0.01 
            
            if scale < 0.1:
                scale = 0.1

        gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
    
        glScalef(scale, scale, scale)
    
    elif camera_mode == 2:
    
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle
            
            if phi < -89.0:
                phi = -89.0
            if phi > 89.0:
                phi = 89.0
            
        fx = math.cos(math.radians(theta)) * math.cos(math.radians(phi))
        fy = math.sin(math.radians(phi))
        fz = math.sin(math.radians(theta)) * math.cos(math.radians(phi))
        
        gluLookAt(eye[0], eye[1], eye[2],
              eye[0] + fx, eye[1] + fy, eye[2] + fz, 0.0, 1.0, 0.0)
        

    axes()
    example_object()
    
    delta_x = 0
    delta_y = 0

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
    global camera_mode
    
    fx = math.cos(math.radians(theta)) * math.cos(math.radians(phi))
    fy = math.sin(math.radians(phi))
    fz = math.sin(math.radians(theta)) * math.cos(math.radians(phi))
    
    rx = -fz
    rz = fx
    
    length = math.hypot(rx, rz)
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
         glfwSetWindowShouldClose(window, GLFW_TRUE)
         
    if key == GLFW_KEY_Q and action == GLFW_PRESS:
        camera_mode = (camera_mode + 1) % 3
        
    if key == GLFW_KEY_W and (action == GLFW_PRESS or action == GLFW_REPEAT):
        eye[0] += fx * move_speed
        eye[1] += fy * move_speed
        eye[2] += fz * move_speed
    
    if key == GLFW_KEY_S and (action == GLFW_PRESS or action == GLFW_REPEAT):
        eye[0] -= fx * move_speed
        eye[1] -= fy * move_speed
        eye[2] -= fz * move_speed
        
    if key == GLFW_KEY_A and (action == GLFW_PRESS or action == GLFW_REPEAT):
        if length > 0:
            eye[0] -= (rx / length) * move_speed
            eye[2] -= (rz / length) * move_speed
        
    if key == GLFW_KEY_D and (action == GLFW_PRESS or action == GLFW_REPEAT):
        if length > 0:
            eye[0] += (rx / length) * move_speed
            eye[2] += (rz / length) * move_speed


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
        left_mouse_button_pressed = 0
        
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_RELEASE:
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
