import sys

from glfw.GLFW import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

#region paramiters
N = 20
tab = np.zeros((N, N, 3))
colors = np.zeros((N, N, 3))
random.seed(0)
#endregion

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    egg()
    eggColors()


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)
    #x
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)
    #y
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)
    #z
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()
def eggColors():
    for i in range(N):
        for j in range(N):
            colors[i][j][0] = random.random()
            colors[i][j][1] = random.random()
            colors[i][j][2] = random.random()
    for i in range(N):
        colors[i][0] = colors[N - 1 - i][N - 1]

def egg():
    for i in range(N):
        u = i / (N - 1)  
        for j in range(N):
            v = j / (N - 1)  
            # x,y,z
            tab[i][j][0] = ( -90 * pow(u, 5) + 225 * pow(u, 4) - 270 *  pow(u, 3) + 180 *  pow(u, 2) - 45 * u) * cos(pi * v)
            tab[i][j][1] = 160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2) - 5
            tab[i][j][2] = ( -90 * pow(u, 5) + 225 * pow(u, 4) - 270 *  pow(u, 3) + 180 *  pow(u, 2) - 45 * u) * sin(pi * v)

#region Render
def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin (time* 180 / pi)

    # glColor3f(1.0, 1.0, 1.0)

    # glBegin(GL_TRIANGLES)
    # glBegin(GL_LINES)
    # glBegin(GL_POINTS)
    for i in range (N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
        
            glColor3fv(colors[i][j])  
            glVertex3fv(tab[i][j])    
            glColor3fv(colors[i+1][j])
            glVertex3fv(tab[i+1][j])  

            # trojkaty i N-1, j N-1
            # glColor3fv(colors[i][j])  
            # glVertex3fv(tab[i][j]) 
            # glColor3fv(colors[i+1][j])
            # glVertex3fv(tab[i+1][j])
            # glColor3fv(colors[i][j+1])
            # glVertex3fv(tab[i][j+1])        

            # #dopelnienie
            # glColor3fv(colors[i+1][j])
            # glVertex3fv(tab[i+1][j])
            # glColor3fv(colors[i][j+1])
            # glVertex3fv(tab[i][j+1])
            # glColor3fv(colors[i+1][j+1])
            # glVertex3fv(tab[i+1][j+1])  
        
            #linie
            # glColor3fv(colors[i][j])  
            # glVertex3f(*tab[i][j])
            # glColor3fv(colors[i][j+1])  
            # glVertex3f(*tab[i][j+1])
            
            # glColor3fv(colors[i+1][j])  
            # glVertex3f(*tab[i+1][j])
            # glColor3fv(colors[i][j])  
            # glVertex3f(*tab[i][j])
            # glVertex3f(*tab[i][j])  
        glEnd()

    axes()

    glFlush()
#endregion
def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

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
