import sys
import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 1 - trojkat, 2 - prostokat, 3 - losowosc prostokat
AKTUALNE_ZADANIE = 3

def draw_trojkat():
    glBegin(GL_TRIANGLES)  
    glColor3f(1.0, 0.2, 0.2)
    glVertex2f(-60.0, -60.0)
    glColor3f(0.2, 1.0, 0.2)
    glVertex2f(60.0, -60.0)
    glColor3f(0.2, 0.2, 1.0)
    glVertex2f(0.0, 60.0)
    glEnd()  

def draw_prostokat(px, py, w, h, deform=0.0):
    w_def = w * (1.0 + deform)  # szerokosc po deformacji
    h_def = h * (1.0 + deform)  # wysokosc po deformacji
    
    trojkat1 = (random.random(), random.random(), random.random()) 
    trojkat2 = (random.random(), random.random(), random.random())
    
    glBegin(GL_TRIANGLES)  
    glColor3f(*trojkat1)
    glVertex2f(px, py)
    glVertex2f(px + w_def, py)
    glVertex2f(px, py + h_def)
    
    glColor3f(*trojkat2)
    glVertex2f(px + w_def, py)
    glVertex2f(px + w_def, py + h_def)
    glVertex2f(px, py + h_def)
    glEnd() 

def startup():
    update_viewport(None, 600, 600)  
    glClearColor(0.0, 0.0, 0.0, 1.0)  #kolor tla

def shutdown():
    pass  

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(4250)

    if AKTUALNE_ZADANIE == 1:  #zad 1
        draw_trojkat()  
    elif AKTUALNE_ZADANIE == 2:  #zad 2
        draw_prostokat(-40.0, -40.0, 80.0, 50.0, 0.0)  
    elif AKTUALNE_ZADANIE == 3:  # zad 3
        draw_prostokat(-50.0, -31.25, 80.0, 50.0, 0.25) # 0.25 - deformacja 

    glFlush()

def update_viewport(window, width, height):
    if width == 0: width = 1  
    if height == 0: height = 1  
    aspect = width / height  

    glMatrixMode(GL_PROJECTION)  
    glViewport(0, 0, width, height)  
    glLoadIdentity()  

    if width <= height:  
        glOrtho(-100.0, 100.0, -100.0 / aspect, 100.0 / aspect, 1.0, -1.0)  
    else:  
        glOrtho(-100.0 * aspect, 100.0 * aspect, -100.0, 100.0, 1.0, -1.0)  

    glMatrixMode(GL_MODELVIEW)  
    glLoadIdentity()  

def main():
    if not glfwInit():  
        sys.exit(1)  

    win = glfwCreateWindow(600, 600, "laboratorium 2 - grafika [Jakub Lefek 284413]", None, None)  
    if not win:  
        glfwTerminate()
        sys.exit(1)

    glfwMakeContextCurrent(win)  
    glfwSetFramebufferSizeCallback(win, update_viewport)  
    glfwSwapInterval(1)  

    startup()  
    while not glfwWindowShouldClose(win):  
        render(glfwGetTime())  
        glfwSwapBuffers(win)  
        glfwPollEvents()  
        
    shutdown() 
    glfwTerminate() 

if __name__ == '__main__':  
    main()
