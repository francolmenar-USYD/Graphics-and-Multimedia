from OpenGL.GL import *
from OpenGL.GLU import *
BaseContext = testingcontext.getInteractive()
from OpenGL.GLUT import *


def init():
    glClearColor(0.0, 0.0, 0.0, 0)

    glClearDepth(10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # glOrtho(-10, 10, -10, 10, 10, -10, 10)

    # gluPerspective(25, 1, 0.1, 50)
    # gluLookAt(10, 10, 10, 0, 0, 0, 0, 1, 0)
    # glTranslate(0.0,10,0)
    # glEnable(GL_DEPTH_TEST)


def display_1():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rad = 30

    glPushMatrix()
    glColor3f(1.0, 0.8, 0.3)
    glutSolidSphere(rad, 50, 50)
    glPopMatrix()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)  # Display mode
glutInitWindowSize(700, 700)
glutCreateWindow(b'Solar system')
glutDisplayFunc(display_1)
glutIdleFunc(display_1)
glutMainLoop()
init()
