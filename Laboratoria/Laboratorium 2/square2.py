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

                

def render(time):

    glClear(GL_COLOR_BUFFER_BIT)

    random.seed(int(time))
    square(*param)

    
    glFlush()

def square(x, y, a, b, d=0.0):
    if (d!=0):
        a= a*d
        b= b-d
    glColor3f(random.random(), random.random(), random.random())
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+a, y)
    glVertex2f(x, y - b)
    glEnd()

    # glColor3f(0.0,g, b)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + a, y)
    glVertex2f(x , y - b)
    glVertex2f(x + a, y - b)
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

    
    param [0] = float (input("podaj x\n"))
    param [1] = float (input("podaj y\n"))
    param [2] = float (input("podaj a\n"))
    param [3] = float (input("podaj b\n"))
    param [4] = float (input("podaj d\n"))


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
