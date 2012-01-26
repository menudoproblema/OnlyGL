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


class Viewport(object):
    def __init__(self, width, height):
        self._width = int(width)
        self._height = int(height)
        self._calculate_aspect()

    def _calculate_aspect(self):
        self._aspect = float(self._width) / float(self._height)

    def _get_width(self):
        return self._width
    def _set_width(self, value):
        self._width = int(value)
        self._calculate_aspect()
    width = property(_get_width, _set_width)

    def _get_height(self):
        return self._height
    def _set_height(self, value):
        self._height = int(value)
        self._calculate_aspect()
    height = property(_get_height, _set_height)

    def _get_aspect(self):
        return self._aspect
    def _set_aspect(self, value):
        pass # Ignore
    aspect = property(_get_aspect, _set_aspect)

    def set_size(self, width, height):
        self._width = int(width)
        self._height = int(height)
        self._calculate_aspect()
