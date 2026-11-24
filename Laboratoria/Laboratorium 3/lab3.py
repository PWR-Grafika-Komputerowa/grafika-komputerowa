#!/usr/bin/env python3
import sys
import math
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

ZADANIE = 5

N = 30
tab = [[[0.0] * 3 for i in range(N)] for j in range(N)]
colors = [[[0.0] * 3 for i in range(N)] for j in range(N)]

def generate_egg():
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v) 
            
            colors[i][j][0] = random.random()
            colors[i][j][1] = random.random()
            colors[i][j][2] = random.random()
            
            tab[i][j][0] = x
            tab[i][j][1] = y
            tab[i][j][2] = z
            
    for i in range(N):
        colors[i][N - 1] = colors[N - 1 - i][0]
        
def zadanie_1():
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    
    for i in range(N):
        for j in range(N):
            glVertex3fv(tab[i][j])
    glEnd()
            
def zadanie_2():
    glBegin(GL_LINES)
    glColor3f(0.5, 0.0, 1.0)
    
    for i in range(N-1):
        for j in range(N-1):
            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i + 1][j])
            
            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i][j + 1])
    glEnd()
    
def zadanie_3():
    glBegin(GL_TRIANGLES)
    
    for i in range(N-1):
        for j in range(N-1):
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])
            
            glColor3fv(colors[i+1][j])
            glVertex3fv(tab[i + 1][j])
            
            glColor3fv(colors[i][j+1])
            glVertex3fv(tab[i][j + 1])
            
            
            glColor3fv(colors[i+1][j+1])
            glVertex3fv(tab[i+1][j + 1])
            
            glColor3fv(colors[i+1][j])
            glVertex3fv(tab[i + 1][j])
            
            glColor3fv(colors[i][j+1])
            glVertex3fv(tab[i][j + 1])
    glEnd()
    
def zadanie_4():
    for i in range(N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])
            
            glColor3fv(colors[i+1][j])
            glVertex3fv(tab[i+1][j])
        glEnd()

def draw_sphere(radius, color):
    glColor3fv(color)
    n_sphere = 20
    
    for i in range(n_sphere):
        phi1 = -math.pi / 2 + i * math.pi / n_sphere
        phi2 = -math.pi / 2 + (i + 1) * math.pi / n_sphere
        
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(n_sphere + 1):
            theta = j * 2 * math.pi / n_sphere
            
            x1 = radius * math.cos(phi1) * math.cos(theta)
            y1 = radius * math.sin(phi1)
            z1 = radius * math.cos(phi1) * math.sin(theta)
            glVertex3f(x1, y1, z1)
            
            x2 = radius * math.cos(phi2) * math.cos(theta)
            y2 = radius * math.sin(phi2)
            z2 = radius * math.cos(phi2) * math.sin(theta)
            glVertex3f(x2, y2, z2)
        glEnd()

def draw_orbit_line(r_x, r_z):
    glBegin(GL_LINE_LOOP)
    glColor3f(0.4, 0.4, 0.4)
    for i in range(100):
        angle = i * 2 * math.pi / 100
        x = r_x * math.cos(angle)
        z = r_z * math.sin(angle)
        glVertex3f(x, 0.0, z)
    glEnd()

def draw_planet(time, radius, orbit_x, orbit_z, speed, color):
    draw_orbit_line(orbit_x, orbit_z)

    angle = time * speed

    x = orbit_x * math.cos(angle)
    z = orbit_z * math.sin(angle)

    glPushMatrix()
    glTranslatef(x, 0.0, z)
    glRotatef(time * 50.0, 0.0, 1.0, 0.0)
    draw_sphere(radius, color)
    glPopMatrix()

def zadanie_5(time):
    glRotatef(20.0, 1.0, 0.0, 0.0)

    glPushMatrix()
    glRotatef(time * 20.0, 0.0, 1.0, 0.0)
    draw_sphere(0.8, [1.0, 0.8, 0.0])
    glPopMatrix()

    draw_planet(time, radius=0.2, orbit_x=2.5, orbit_z=2.0, speed=2.0, color=[0.2, 0.6, 1.0])
    draw_planet(time, radius=0.3, orbit_x=4.5, orbit_z=3.8, speed=1.0, color=[0.2, 0.8, 0.3])
    draw_planet(time, radius=0.4, orbit_x=6.5, orbit_z=5.5, speed=0.5, color=[0.9, 0.3, 0.2])

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    generate_egg()


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
    
def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if ZADANIE == 5:
        zadanie_5(time)
    else:
        axes()
        
        angle = time * 180 / math.pi
        spin(angle)
        
        if ZADANIE == 1:
            zadanie_1()
        elif ZADANIE == 2:
            zadanie_2()
        elif ZADANIE == 3:
            zadanie_3()
        elif ZADANIE == 4:
            zadanie_4()

    glFlush()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


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
