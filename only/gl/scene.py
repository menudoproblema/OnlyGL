"""
This file is part of OnlyGL.

OnlyGL is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OnlyGL is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OnlyGL.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2011 Vicente Ruiz Rodriguez <vruiz2.0@gmail.com>
"""


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.constant import Constant
GLUT_WHEEL_UP = Constant('GLUT_WHEEL_UP', 3)
GLUT_WHEEL_DOWN = Constant('GLUT_WHEEL_DOWN', 4)
# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

from only.gl.cameras import Camera
from only.gl.lights import Light
from only.gl.viewports import Viewport


class MouseState(object):
    def __init__(self, button=None, state=None, pressed=False, x=0, y=0):
        self.button = button
        self.state = state
        self.pressed = pressed
        self.x = x
        self.y = y

class Scene(object):
    def __init__(self, viewport_width=600, viewport_height=600,
                 camera=None, enable_lighting=True, lights=[]):
        if camera:
            self.camera = camera
        else:
            self.camera = Camera(
                [15.0, 10.0, 30.0],
                [0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
            )
        self.viewport = Viewport(viewport_width, viewport_height)

        self._xrot = 0.0
        self._yrot = 0.0
        self._zrot = 0.0
        self._scale = 1.0
        self._xdist = 0.0
        self._ydist = 0.0
        self._zdist = 0.0

        self.init_model()
        self.mouse_state = MouseState()

        self._enabled_lighting = enable_lighting
        if len(lights) > 0:
            self.lights = lights
        else:
            self.lights = (Light(GL_LIGHT0), )

    def init_model(self):
        raise Exception('Unimplemented')

    def draw(self):
        raise Exception('Unimplemented')

    def motionfunc(self, button, state, x, y):
        raise Exception('Unimplemented')

    def _transfomations(self):
        glTranslatef(self._xdist, self._ydist, self._zdist) # Move Into The Screen
        glRotatef(self._xrot, 1.0, 0.0, 0.0)    # Rotate The Cube On It's X Axis
        glRotatef(self._yrot, 0.0, 1.0, 0.0)    # Rotate The Cube On It's Y Axis
        glRotatef(self._zrot, 0.0, 0.0, 1.0)    # Rotate The Cube On It's Z Axis
        glScalef(self._scale, self._scale, self._scale)

    def init(self):
        # Light source
        self.enable_lighting()

        # Initialize OpenGL
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_CULL_FACE)
        glShadeModel(GL_FLAT)
        # Transparencies
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glInitNames()
        glPushName(-1)

    def enable_lighting(self):
        if self._enabled_lighting:
            glEnable(GL_LIGHTING)
            for light in self.lights:
                light.enable()

            self._enabled_lighting = True

    def disable_lighting(self):
        if not self._enabled_lighting:
            glDisable(GL_LIGHTING)
            for light in self.lights:
                light.disable()

            self._enabled_lighting = False

    def perspective(self):
        gluPerspective(45.0, self.viewport.aspect, 1.5, 1500)
        gluLookAt(*self.camera.coordinates)

    def reshapefunc(self, width, height):
        self.viewport.set_size(width, height)
        glViewport(0, 0, width, height)

    def displayfunc(self):
        # Initialize
        glClearColor(0.0, 0.0, 0.6, 1.0) # Fija el color de fondo a azul
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ## Projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.perspective()

        ## Modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()

        # Draw the scene
        self._transfomations()
        self.draw()

        glPopMatrix()

        glutSwapBuffers()
        #glFlush()

    def keyboardfunc(self, *args):
        import sys
        # If escape is pressed, kill everything.
        if args[0] == ESCAPE:
            sys.exit()

    def mousefunc(self, button, state, x, y):
        self.mouse_state.button = button
        self.mouse_state.state = state
        self.mouse_state.x = x
        self.mouse_state.y = y

        if button == GLUT_WHEEL_DOWN:
            self._scale *= 1.1
            return
        elif button == GLUT_WHEEL_UP:
            self._scale /= 1.1
            return

    def pick(self, x, y):
        glSelectBuffer(128)
        glRenderMode(GL_SELECT) # Realizamos la visualizacion en modo seleccion

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        viewport = glGetIntegerv(GL_VIEWPORT)
        # 5x5 window size
        gluPickMatrix(x, viewport[3]-y, 5, 5, viewport)
        self.perspective()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self._transfomations()
        self.draw()

        # Getting the nearest
        records = glRenderMode(GL_RENDER)
        nearest = float('inf')
        record = None

        for hit_record in records:
            near, far, names = hit_record
            if near < nearest:
                nearest = near
                record = names
        return record

    def get_world_coordinates(self, x, y):
        """Get the world coordinates from the screen coordinates."""
        model_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        project_matrix = glGetDoublev(GL_PROJECTION_MATRIX)

        viewport = glGetIntegerv(GL_VIEWPORT)

        win_x = int(x)
        win_y = int(viewport[3] - y)
        win_z = glReadPixels(win_x, win_y, 1, 1, GL_DEPTH_COMPONENT,
            GL_FLOAT)

        real_x, real_y, real_z = gluUnProject(win_x, win_y, win_z,
            model_matrix, project_matrix, viewport)

        return (
            real_x/self._scale,
            real_y/self._scale,
            real_z/self._scale
        )
