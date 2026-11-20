#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy
import math

#
#   Zadanie 3.2 - Symulacja ruchu planet  
#

N_vertex = 10

def x(u,v,R):
    return R*math.sin(math.pi*u)*math.cos(2*math.pi*v)

def y(u,v,R):
    return R*math.cos(math.pi*u)

def z(u,v,R):
    return R*math.sin(math.pi*u)*math.sin(2*math.pi*v)

def sphereVertex(tab, N, R):      # wyznaczanie wspolrzednych punktow dla modelu sfery
    for u in range(N):
        for v in range(N):
            tab[u,v,0] = x(u/(N-1),v/(N-1),R)     # wartosc x
            tab[u,v,1] = y(u/(N-1),v/(N-1),R)     # wartosc y
            tab[u,v,2] = z(u/(N-1),v/(N-1),R)     # wartosc z

def Sphere(N,R,color):         # budowanie modelu sfery z trojkatow
    tab = numpy.zeros((N, N, 3))
    sphereVertex(tab,N,R)
    glBegin(GL_TRIANGLES)
    for u in range(N-1):
        for v in range(N-1):
            glColor3fv(color)
            glVertex3fv(tab[u,v])
            glVertex3fv(tab[u+1,v])
            glVertex3fv(tab[u,v+1])

            glVertex3fv(tab[u+1,v+1])
            glVertex3fv(tab[u+1,v])
            glVertex3fv(tab[u,v+1])
    glEnd()

def calculatePeriod(a):     # III prawo Keplera
    return a**1.5

def planetPosition(a,e,time,period):    # II prawo Keplera
    M = 2*math.pi*time/period   # anomalia srednia (angle)
    M = M%(2*math.pi)   # jeden obieg
    
    # przyblizone rozwiazanie rownania Keplera
    E = M

    # wykorzystanie metody polowienia przedzialu
    # przedzial rozwiazania [left;right]
    left = 0.0
    right = 2*math.pi

    # iteracyjne wyznaczanie przyblizenia E
    for i in range(50):
        E = (left+right)/2      # polowienie z (nowego) przedzialu

        f = E-e*math.sin(E)-M     # wyznaczenie przyblizenia

        if f > 0:       # wybor jednego z dwoch przedzialow
            right = E
        else:
            left = E

    b = a*math.sqrt(1-e**2) # mala polos

    # wspolrzedne planety
    px = a*(math.cos(E)-e)
    py = b*math.sin(E)

    return px, py

def ellipse(a,e):   # rysowanie orbity - I prawo Keplera
    b = a*math.sqrt(1-e**2) # mala polos
    glBegin(GL_LINES)
    glColor3f(0.5,0.5,0.5)

    for i in range(200):
        angle = 2*math.pi*i/200
        px = a*(math.cos(angle)-e)
        py = b*math.sin(angle)
        glVertex3f(px,py,0.0)

    glEnd()

planets = [
    {
        "a": 2.0,       # wielka polos
        "e": 0.6,       # mimosrod orbity (eliptycznosc orbity)
        "radius": 0.15,     # promien planety
        "color": (1.0,0.5,0.0)
    },
    {
        "a": 3.5,
        "e": 0.6,
        "radius": 0.22,
        "color": (0.0,0.8,0.0)
    },
    {
        "a": 5.0,
        "e": 0.5,
        "radius": 0.3,
        "color": (0.0,0.5,1.0)
    }
]

def startup():
    update_viewport(None, 600, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def spin(angle):        # animacja obiektu
    glRotate(5*angle, 1.0, 0.0, 0.0)
    #glRotate(15*angle, 0.0, 1.0, 0.0)
    glRotate(5*angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    Sphere(N_vertex, 0.5, (1.0, 1.0, 0.0))  # Slonce

    spin(time)    # widok z boku

    for planet in planets:  # planety na orbicie

        a = planet["a"]
        e = planet["e"]
        radius = planet["radius"]
        color = planet["color"]

        period = calculatePeriod(a) # III prawo Keplera
        ellipse(a,e)   # orbita planety

        # aktualne polozenie planety
        px,py = planetPosition(a,e,time,period)

        # zapisanie aktualnej macierzy transformacji
        glPushMatrix()

        # przesuniecie ukladu wspolrzednych
        glTranslatef(px,py,0.0)

        # rysowanie modelu planety
        Sphere(N_vertex,radius,color)

        # przywrocenie wczesniej zapisanej macierzy transformacji
        glPopMatrix()

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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 15, -15)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 15, -15)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(600, 400, __file__, None, None)
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