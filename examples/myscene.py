from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from only.gl import colors
from only.gl.scene import Scene


class MyScene(Scene):

    def init_model(self):
        self.x = 0.0
        self.y = -0.5
        self.z = 0.0
        self.color = colors.GREEN

    def draw(self):
        # Draw the floor
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
        glTranslatef(self.x, self.y, self.z)
        self.draw_box(200.0, 0.5, 200.0)
        # And your model

    def draw_box(self, a, b, m):
        x = float(a) / 2.0
        z = float(m) / 2.0
        y = float(b)

        glShadeModel(GL_FLAT)

        glBegin(GL_QUAD_STRIP)

        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(x, 0, -z)
        glVertex3f(-x, 0, -z)
        glVertex3f(x, y, -z)
        glVertex3f(-x, y, -z)

        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(x, y, z)
        glVertex3f(-x, y, z)

        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(x, 0, z)
        glVertex3f(-x, 0, z)

        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(x, 0, -z)
        glVertex3f(-x, 0, -z)

        glEnd()

        glBegin(GL_QUADS)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(x, 0, -z)
        glVertex3f(x, y, -z)
        glVertex3f(x, y, z)
        glVertex3f(x, 0, z)
        glEnd()

        glBegin(GL_QUADS)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-x, 0, -z)
        glVertex3f(-x, 0, z)
        glVertex3f(-x, y, z)
        glVertex3f(-x, y, -z)
        glEnd()


def main():
    glutInit(sys.argv)

    scene = MyScene()

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(scene.viewport.width, scene.viewport.height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("My first Scene with OnlyGL")

    scene.init()

    glutDisplayFunc(scene.displayfunc)
    glutReshapeFunc(scene.reshapefunc)
    glutKeyboardFunc(scene.keyboardfunc)
    glutMouseFunc(scene.mousefunc)

    glutMainLoop()


print "Hit ESC key to quit."
main()
