
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


daysInYear = 365
year = 0.0
day = 0.0
moonAroundEarth = 0.0
moonItsSelf = 0.0



def init():
	glClearColor(0.0, 0.0, 0.0, 0)

	glClearDepth(10.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	#glOrtho(-10, 10, -10, 10, 10, -10, 10)

	# gluPerspective(25, 1, 0.1, 50)
	# gluLookAt(10, 10, 10, 0, 0, 0, 0, 1, 0)
	#glTranslate(0.0,10,0)
	#glEnable(GL_DEPTH_TEST)


def display_1():
	global day, year, moonItsSelf, moonAroundEarth

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	#
	#
	# glMatrixMode(GL_MODELVIEW)
	# glLoadIdentity()

	# sun
	sunradius = 0.4
	rotationSpeed = 0.3
	earthRadius = 0.06
	moonRadius = 0.016
	moonAroundEarthRate = 2 * rotationSpeed
	moonRotationItselfRate = 5.0 * rotationSpeed
	earthOrbitRadius = 1.0
	moonOrbitRadius = 0.1
	dayRate = 5.0 * rotationSpeed
	yearRate = daysInYear / 360.0 * dayRate * rotationSpeed
	glPushMatrix()
	glColor3f(1.0, 0.8, 0.3)
	glutSolidSphere(sunradius, 50, 50)

	glRotatef(year, 0.0, 1.0, 0.0)
	glTranslatef(earthOrbitRadius, 0.0, 0.0)# translation
	glRotatef(-year, 0.0, 1.0, 0.0)
	glPushMatrix()
	glRotatef(day, 0.25, 1.0, 0.0)
	glColor3f(0.4, 0.6, 0.3)
	glutSolidSphere(earthRadius, 10, 10)
	glPopMatrix()
	glRotatef(moonAroundEarth, 0.0, 1.0, 0.0)
	glTranslatef(moonOrbitRadius, 0.0, 0.0)
	glRotatef(-moonAroundEarth, 0.0, 1.0, 0.0)
	glRotatef(moonItsSelf, 0.0, 1.0, 0.0)
	glColor3f(0.3, 0.3, 0.5)
	glutSolidSphere(moonRadius, 8, 8)
	glPopMatrix()
	glutSwapBuffers()
	# glViewport(0, 0, 200, 200)
	day += dayRate
	year += yearRate
	moonItsSelf += moonRotationItselfRate
	moonAroundEarth += moonAroundEarthRate


glutInit()
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH) # Display mode
glutInitWindowSize(700, 700)
glutCreateWindow(b'Solar system')
glutDisplayFunc(display_1)
glutIdleFunc(display_1)
glutMainLoop()
init()