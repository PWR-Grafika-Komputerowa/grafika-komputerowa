import sys
import random 

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

#region paramiters
r = random.random()
g = random.random()
b = random.random()
iteration 
param = [0] * 5
COLOR = (r,g,b)
WHITE = (1.0,1.0,1.0)
random.seed()
#endregion

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def carpet(x, y, a, b, i):
    am= a/3
    bm= b/3
    for w in range(3):
        for q in range (3):
            if w== 1 and q == 1:
                glColor3f(*WHITE)
                square (x + am*w,y- bm*q,am,bm)
            elif i>0:
                carpet(x + am*w,y- bm*q,am,bm, i-1)
                

def render(time):

    glClear(GL_COLOR_BUFFER_BIT)

    # movingTriangle(-time)
    # squareTime(*param)
    glColor3fv(COLOR)
    square (-100, 100, 200, 200)
    if iteration>0:
        carpet(-100, 100, 200, 200, iteration-1)
    
    glFlush()

def square(x, y, a, b):
 
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+a, y)
    glVertex2f(x, y-b)
    glEnd()

    # glColor3f(r,g, b)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + a, y)
    glVertex2f(x , y - b)
    glVertex2f(x + a, y-b)
    glEnd() 

def squareTime(x, y, a, b, d = 0.0):

    a += d
    b += d 
    glColor3fv(COLOR)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+a, y)
    glVertex2f(x, y+b)
    glEnd()

    # glColor3f(r,g, b)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + a, y)
    glVertex2f(x , y + b)
    glVertex2f(x + a, y+b)
    glEnd()  

def movingTriangle(time):
    if(sin(time) < 1 and cos(time) <0 ):
        bottomTriangle(time)
        rightTriangle(time)
        leftTriangle(time)
    elif (sin(time) >0 and cos(time) <1 ):
        rightTriangle(time)
        leftTriangle(time)
        bottomTriangle(time)
    else:
        leftTriangle(time)
        rightTriangle(time)
        bottomTriangle(time)
    

def rightTriangle(time):
    # (sin(y+pi)+1)/2
    # prawy zielony
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(sin(time)*50, cos(time)*50)
    glVertex2f(0.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd() 

def bottomTriangle(time):
    # dolny niebieski
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(sin(time)*50, cos(time)*50)
    glVertex2f(50.0, 0.0)
    glVertex2f(-50.0, 0.0)
    glEnd()  

def leftTriangle(time):
    # lewy czerwony
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(sin(time)*50, cos(time)*50)
    glVertex2f(0.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()


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



def main():

    
    # param [0] = float (input("podaj x\n"))
    # param [1] = float (input("podaj y\n"))
    # param [2] = float (input("podaj a\n"))
    # param [3] = float (input("podaj b\n"))
    global iteration
    iteration = float (input("podaj i\n"))

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
