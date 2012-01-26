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


class Camera(object):
    def __init__(self, position, look_at, look_up):
        self.position = position
        self.look_at = look_at
        self.look_up = look_up

    def _get_coordinates(self):
        return list(self.position + self.look_at + self.look_up)
    def _set_coordinates(self, value):
        pass # Ignore
    coordinates = property(_get_coordinates, _set_coordinates)
