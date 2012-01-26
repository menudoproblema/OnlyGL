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


class Light(object):
    def __init__(self, name,
                 x=15.0, y=10.0, z=10.0, w=0.0,
                 ambient=(0.0, 0.0, 0.0, 1.0),
                 diffuse=(1.0, 1.0, 1.0, 1.0),
                 specular=(1.0, 1.0, 1.0, 1.0)):
        # Position & name
        self._position = (x, y, z, w)
        self.name = name
        # Ambient, diffuse and specular values
        self.ambient = tuple(ambient)
        self.diffuse = tuple(diffuse)
        self.specular = tuple(specular)

    def set_directional(self):
        x, y, z, w = self._position
        self._position = (x, y, z, 0.0)

    def set_positional(self):
        x, y, z, w = self._position
        self._position = (x, y, z, 1.0)

    def enable(self):
        glEnable(self.name)
        glLightfv(self.name, GL_AMBIENT, self.ambient)
        glLightfv(self.name, GL_DIFFUSE, self.diffuse)
        glLightfv(self.name, GL_SPECULAR, self.specular)
        glLightfv(self.name, GL_POSITION, self.position)

    def disable(self):
        glDisable(self.name)

    def _get_position(self):
        return self._position
    def _set_position(self, value):
        pass # Ignore
    position = property(_get_position, _set_position)

    def _get_x(self):
        return self._position[0]
    def _set_x(self, value):
        x, y, z, w = self._position
        self._position = (value, y, z, w)
    x = property(_get_x, _set_x)

    def _get_y(self):
        return self._position[1]
    def _set_y(self, value):
        x, y, z, w = self._position
        self._position = (x, value, z, w)
    y = property(_get_y, _set_y)

    def _get_z(self):
        return self._position[2]
    def _set_z(self, value):
        x, y, z, w = self._position
        self._position = (x, y, value, w)
    z = property(_get_z, _set_z)

