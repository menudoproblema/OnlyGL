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


import math
from OpenGL.GL import *

from only.gl import colors


class Model(object):
    def __init__(self, x=0.0, y=0.0, z=0.0, name=None, color=None):
        # Position
        self.x = x
        self.y = y
        self.z = z
        # Color and name
        self.color = color
        self.name = name
        self._selected = False

    def is_selected(self):
        return self._selected

    def set_selected(self, value):
        self._selected = value

    def model(self):
        raise Exception('Unimplemented')

    def _transfomations(self):
        glTranslatef(self.x, self.y, self.z)

    def draw(self):
        # Setting the name
        if self.name is not None:
            glPushName(self.name)

        # Choosing the color
        if self._selected:
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, colors.HIGHLIGHT)
        elif self.color:
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)

        # Drawing the model
        glPushMatrix()
        self._transfomations()
        self.model()
        glPopMatrix()

        # Restoring previous name
        if self.name is not None:
            glPopName()

    def collision(self, obj, xyz=False):
        """Detecta colisiones con otro objeto."""
        raise Exception('Unimplemented')


class BoxModel(Model):
    def __init__(self, width, height, depth,
                 x_angle=0.0, y_angle=0.0, z_angle=0.0, **kwargs):
        super(BoxModel, self).__init__(**kwargs)
        # Box properties
        self.width = width
        self.height = height
        self.depth = depth
        # Angle properties
        self.x_angle = x_angle
        self.y_angle = y_angle
        self.z_angle = z_angle

    def _transfomations(self):
        super(BoxModel, self)._transfomations()
        glRotatef(self.x_angle, 1.0, 0.0, 0.0)
        glRotatef(self.y_angle, 0.0, 1.0, 0.0)
        glRotatef(self.z_angle, 0.0, 0.0, 1.0)

    def collision(self, obj, xyz=False):
        """
        Detecta colisiones de cualquier objeto que tenga atributos x, y,
        z, width, height y depth. La colision se puede comprobar en dos
        dimensiones (x, z) o en tres dimensiones (x, y, z).
        """
        x = math.fabs(self.x - obj.x)
        width = self.width*0.5 + obj.width*0.5
        z = math.fabs(self.z - obj.z)
        depth = self.depth*0.5 + obj.depth*0.5

        xz_collision = x < width and z < depth

        # 2D collision?
        if not xyz:
            return xz_collision

        # 3D collision
        y_collision = obj.y > self.y and obj.y < (self.y + self.height)
        y_collision = y_collision or (
            obj.y < self.y and self.y < (obj.y + obj.height))

        return xz_collision and y_collision
