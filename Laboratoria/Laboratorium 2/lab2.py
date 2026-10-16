#!/usr/bin/env python3
import sys
import random
import collections
import time as tm
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.05, 0.05, 0.05, 1.0)


def shutdown():
    pass

Point = collections.namedtuple('Point',  ['x', 'y', 'c'])

_s = 1
_sMax = 10
_frame = 1

def render(time):
    global _s
    global _sMax
    global _frame
    global Point
    glClear(GL_COLOR_BUFFER_BIT)
    
    #sierpinski(0, 0, 200, 200, _s)
    
    plasma_start(0,0,200,200,_s)
    
    tm.sleep(1)
    _s += 1
    #if _frame >= 121:
    #    _s += 1
    #    _frame = 0
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

def plasma_start(x, y, a, b, s):
    c1 = Point(x - (a/2),y + (b/2), random.random())
    c2 = Point(x + (a/2),y + (b/2), random.random())
    c3 = Point(x - (a/2),y - (b/2), random.random())
    c4 = Point(x + (a/2),y - (b/2), random.random())
    
    
    glBegin(GL_TRIANGLES)
    glColor3f(c1.c, c1.c, c1.c)
    glVertex2f(c1.x, c1.y)
    glColor3f(c2.c, c2.c,c2.c)
    glVertex2f(c2.x, c2.y)
    glColor3f(c3.c, c3.c, c3.c)
    glVertex2f(c3.x, c3.y)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(c4.c, c4.c, c4.c)
    glVertex2f(c4.x, c4.y)
    glColor3f(c2.c, c2.c, c2.c)
    glVertex2f(c2.x, c2.y)
    glColor3f(c3.c, c3.c, c3.c)
    glVertex2f(c3.x, c3.y)
    glEnd()
    
    plasma(c1,c2,c3,c4,a/2, b/2,s)
    
    
def corner(cxy, cx, cy):
    return (1 - 2 * W(cxy))*cxy  + W(cx)*cx + W(cy)*cy
   
def center(cc, c1,c2,c3,c4):
    return  (1 - 4*Wc(cc)*cc + Wc(c1)*c1 + Wc(c2)*c2 + Wc(c3)*c3 + Wc(c4)*c4)
    
def W(x):
    return 0.53474/(1 + pow(2.71,((x-80)/30)))
def Wc(x):
    return 0.5*W(x)
    
def plasma(c1,c2,c3,c4,a,b,s):
    if s == 0:
        return
    
    c12 = Point((c1.x + c2.x)/2, (c1.y + c2.y)/2, corner(random.random(), c1.c,  c2.c))
    c13 = Point((c1.x + c3.x)/2, (c1.y + c3.y)/2, corner(random.random(), c1.c,  c3.c))
    c24 = Point((c2.x + c4.x)/2, (c2.y + c4.y)/2, corner(random.random(), c2.c,  c4.c))
    c34 = Point((c3.x + c4.x)/2, (c3.y + c4.y)/2, corner(random.random(), c3.c,  c4.c))
    cc  = Point((c1.x + c4.x)/2, (c1.y + c4.y)/2, center(random.random(), c1.c,  c2.c,  c3.c, c4.c))
    
    glBegin(GL_TRIANGLES)
    glColor3f( c12.c, c12.c,c12.c)
    glVertex2f(c12.x, c12.y)
    glColor3f(c13.c, c13.c,c13.c)
    glVertex2f(c13.x, c13.y)
    glColor3f(cc.c,cc.c, cc.c )
    glVertex2f(cc.x, cc.y)
    
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(cc.c, cc.c, cc.c)
    glVertex2f(cc.x, cc.y)
    glColor3f(c24.c, c24.c, c24.c)
    glVertex2f(c24.x, c24.y)
    glColor3f(c34.c, c34.c, c34.c)
    glVertex2f(c34.x, c34.y)
    glEnd()
    
    s-=1
    plasma(c1,c12,c13,cc,a/2,b/2,s)
    plasma(c12,c2,cc,c24,a/2,b/2,s)
    plasma(c13,cc,c3,c34,a/2,b/2,s)
    plasma(cc,c24,c34,c4,a/2,b/2,s)
    
    

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
