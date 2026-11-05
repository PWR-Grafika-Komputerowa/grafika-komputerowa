import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin, pi
import numpy as np




#region variables
N = 20
tab = np.zeros((N, N, 3))
vektors = np.zeros((N, N, 3))

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi=0.0
R=10.0
scale =1.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

index=0
index2=0
mode =0
zmienne =   [
light_ambient  ,
light_diffuse ,
light_specular
]

tryby= [GL_AMBIENT ,
GL_DIFFUSE ,
GL_SPECULAR ]

#endregion
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    egg()

def egg():
    global vektors
    for i in range(N):
        u = i / (N - 1)  
        for j in range(N):
            v = j / (N - 1)  
            # x,y,z
            tab[i][j][0] = ( -90 * pow(u, 5) + 225 * pow(u, 4) - 270 *  pow(u, 3) + 180 *  pow(u, 2) - 45 * u) * cos(pi * v)
            tab[i][j][1] = 160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2) - 5
            tab[i][j][2] = ( -90 * pow(u, 5) + 225 * pow(u, 4) - 270 *  pow(u, 3) + 180 *  pow(u, 2) - 45 * u) * sin(pi * v)

            xu = (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * cos(pi * v)
            xv = pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * sin(pi * v)
            yu = 640 * pow(u, 3) - 960 * pow(u, 2) + 320 * u
            yv = 0
            zu = (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * sin(pi * v)
            zv = -pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * cos(pi * v)    
            vektors[i][j][0] = yu*zv 
            vektors[i][j][1] = (zu * xv) - (zv * xu)
            vektors[i][j][2] = 0 -( xv * yu)

    norm = np.linalg.norm(vektors, axis=2, keepdims=True)
    norm[norm == 0] = 1.0  
    vektors = -(vektors / norm)
    print (vektors)

def shutdown():
    pass

#region render
def render(time):
    global theta,phi,R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if delta_x >1.0 or delta_x < -1.0 or delta_y >1.0 or delta_y < -1.0:
            if left_mouse_button_pressed:
                theta -= delta_x * pix2angle
                phi -= delta_y * pix2angle
    
            if right_mouse_button_pressed:
                R += (delta_x  + delta_y) *  0.01
    # if R < 0.0:
    #     R = 0.0
    # elif R > 10.0:
    #     R = 10.0            
    if phi > 89.0:
        phi = 89.0
    elif phi < -89.0:
        phi = -89.0

    thePI = (theta * (pi / 180.0)) % (2 * pi)
    phiPi = (phi * (pi / 180.0)) % (2 * pi)

    x = R * cos(thePI) * cos(phiPi)
    y = R * sin(phiPi)
    z = R * sin(thePI) * cos(phiPi)

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    light=[x,y,z,1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light)

    glColor3f(0.0, 1.0, 0.0)

    for i in range (N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3fv(vektors[i][j])
            glVertex3fv(tab[i][j])
            glNormal3fv(vektors[i+1][j])    
            glVertex3fv(tab[i+1][j])  
 
        glEnd()
    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)
    # gluDeleteQuadric(quadric)

    glTranslate(x,y,z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glTranslate(-x,-y,-z)

    glFlush()

#endregion
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

#region inputs
def keyboard_key_callback(window, key, scancode, action, mods):
    global zmienne, tryby, index,index2,mode

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_ENTER and action == GLFW_PRESS:
        mode = (mode +1)%2

    if mode == 0:
        if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
            index = (index + 1 )% len(tryby)
        if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
            index = (index - 1 )% len(tryby)
        print("zmiana trybu")
    if mode == 1:
        if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
            index2 = (index2 + 1 )% 4
        if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
            index2 = (index2 - 1 )% 4

        if key == GLFW_KEY_UP and action == GLFW_PRESS: 
            zmienne[index][index2] += 0.1  
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            zmienne[index][index2] -= 0.1
          
        if zmienne[index][index2] > 1.0 :
            zmienne[index][index2] = 1.0
        elif zmienne[index][index2] < 0.01 :
            zmienne[index][index2] = 0.0

        glLightfv(GL_LIGHT0, tryby[index], zmienne[index])
        print("zmiana wartosci")
    wypiszNazwe(tryby[index]),print(zmienne[index], "\nzmieniana wartosc:" ,index2+1,'\n')

          
def wypiszNazwe(var):
    name = [k for k, v in globals().items() if v is var][0]
    print(f" {name}")


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
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

#endregion
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
