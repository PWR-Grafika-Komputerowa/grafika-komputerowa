#!/usr/bin/env python3
import sys
import random
import time as tm
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.05, 0.05, 0.05, 1.0)


def shutdown():
    pass

_s = 1
_sMax = 4
_frame = 1

def render(time):
    global _s
    global _sMax
    global _frame
    glClear(GL_COLOR_BUFFER_BIT)
    
    sierpinski(0, 0, 200, 200, _s)
    
    if _frame >= 121:
        _s += 1
        _frame = 0
    if _s >= _sMax:
        _s = 1
    
    _frame += 1
    glFlush()

def rectangle(x, y, a, b, d=0):
    a = a * (1+d)
    b = b * (1+d)
    #glColor3f(random.random(), random.random(), random.random())
    #glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - (a/2), y - (b/2))
    glVertex2f(x - (a/2), y + (b/2))
    glVertex2f(x + (a/2), y + (b/2))
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glVertex2f(x - (a/2), y - (b/2))
    glVertex2f(x + (a/2), y - (b/2))
    glVertex2f(x + (a/2), y + (b/2))
    glEnd()
    
def sierpinski(x, y, a, b, s):
    a /= 3
    b /= 3
    s -= 1
    rectangle(x, y, a, b, 0.0)
    
    if s == 0:
        return
        
    sierpinski(x - a, y - b, a, b, s)
    sierpinski(x    , y - b, a, b, s)
    sierpinski(x + a, y - b, a, b, s)
    
    sierpinski(x - a, y    , a, b, s)
    sierpinski(x + a, y    , a, b, s)
    
    sierpinski(x - a, y + b, a, b, s)
    sierpinski(x    , y + b, a, b, s)
    sierpinski(x + a, y + b, a, b, s)

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

name = ""
def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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
