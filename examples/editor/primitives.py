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


def module(x, y, z):
    return math.sqrt(x*x + y*y + z*z)

def draw_box(a, b, m):
    x = float(a) / 2.0
    z = float(m) / 2.0
    y = float(b)

    glShadeModel(GL_FLAT)

    # Caras transversales
    glBegin(GL_QUAD_STRIP)

    glNormal3f(0.0, 0.0, -1.0) # Vertical hacia atras
    glVertex3f(x, 0, -z)
    glVertex3f(-x, 0, -z)
    glVertex3f(x, y, -z)
    glVertex3f(-x, y, -z)

    glNormal3f(0.0, 1.0, 0.0) # Superior, horizontal
    glVertex3f(x, y, z)
    glVertex3f(-x, y, z)

    glNormal3f(0.0, 0.0, 1.0) # Vertical delantera
    glVertex3f(x, 0, z)
    glVertex3f(-x, 0, z)

    glNormal3f(0.0, -1.0, 0.0) # Inferior
    glVertex3f(x, 0, -z)
    glVertex3f(-x, 0, -z)

    glEnd()

    # Costados
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

def draw_parallelepiped(x0, y0, z0, x1, y1, z1, a, b):
    m = module(x1-x0, y1-y0, z1-z0)
    glPushMatrix()

    glTranslatef(x0, y0, z0)
    glRotatef(
        -180.0*math.atan2((z1-z0),(x1-x0))/math.pi,
        0.0,
        1.0,
        0.0
    )
    glRotatef(
        180.0*math.atan2(
            (y1-y0),
            math.sqrt((x1-x0)*(x1-x0)+(z1-z0)*(z1-z0))
        )/math.pi-90,
        0.0,
        0.0,
        1.0
    )
    draw_box(a, m, b)

    glPopMatrix()

def draw_framework(width, height, depth, n, section=0.08):
    if n < 1:
        raise Exception("Numero de segmentos en estructura menor que 1")

    e = float(height)/float(n)
    y = 0.0
    a2 = float(width)/2.0
    d2 = float(depth)/2.0

    glPushMatrix()

    for i in range(0, n):
        # Barras horizontales
        draw_parallelepiped(-a2, y, -d2, a2, y, -d2, section, section)
        draw_parallelepiped(a2, y, -d2, a2, y, d2, section, section)
        draw_parallelepiped(a2, y, d2, -a2, y, d2, section, section)
        draw_parallelepiped(-a2, y, d2, -a2, y,-d2, section, section)

        # Barras oblicuas
        if i % 2:
            draw_parallelepiped(-a2, y, -d2, a2, y+e, -d2, section, section)
            draw_parallelepiped(a2, y, -d2, a2, y+e, d2, section, section)
            draw_parallelepiped(a2, y, d2, -a2, y+e, d2, section, section)
            draw_parallelepiped(-a2, y, d2, -a2, y+e, -d2, section, section)
        else:
            draw_parallelepiped(a2, y, -d2, -a2, y+e, -d2, section, section)
            draw_parallelepiped(a2, y, d2, a2, y+e, -d2, section, section)
            draw_parallelepiped(-a2, y, d2, a2, y+e, d2, section, section)
            draw_parallelepiped(-a2, y, -d2, -a2, y+e, d2, section, section)

        # Barras verticales
        draw_parallelepiped(-a2,y,-d2, -a2, y+e, -d2, section, section)
        draw_parallelepiped(a2, y, -d2, a2, y+e, -d2, section, section)
        draw_parallelepiped(-a2, y, d2, -a2, y+e, d2, section, section)
        draw_parallelepiped(a2, y, d2, a2,y+e, d2, section, section)

        # Next level
        y=y+e
    # Barras horizontales de terminacion
    draw_parallelepiped(-a2, y, -d2, a2, y,-d2, section, section)
    draw_parallelepiped(a2, y,-d2, a2, y, d2, section, section)
    draw_parallelepiped(a2,y, d2, -a2, y, d2, section, section)
    draw_parallelepiped(-a2, y, d2, -a2, y,-d2, section, section)

    glPopMatrix()


def draw_jib(width, lenght, n, section=0.08):
    if n < 1:
        raise Exception("Numero de segmentos en brazo menor que 2")

    e = float(lenght)/float(n)

    y = 0
    a2 = float(width) / 2.0
    b = math.sqrt(3)*float(width) / 2.0 # Altura del triangulo de la base

    glPushMatrix()
    draw_parallelepiped(0, y, -a2, 0, y, a2, section, section)
    draw_parallelepiped(0, y, -a2, 0, y+e, a2, section, section)
    draw_parallelepiped(0, y, a2, -b, y+e, 0, section, section)
    draw_parallelepiped(0, y, -a2, -b, y+e, 0, section, section)
    draw_parallelepiped(0, y, -a2, 0, y+e, -a2, section, section)
    draw_parallelepiped(0, y, a2, 0, y+e, a2, section, section)
    y=y+e

    for i in range(1, n):
        # Barras horizontales
        draw_parallelepiped(0, y,-a2, 0,y, a2,section,section)
        draw_parallelepiped(0, y, a2,-b,y, 0,section,section)
        draw_parallelepiped(-b, y, 0,  0,y,-a2,section,section)

        # Barras oblicuas
        if i % 2:
            draw_parallelepiped(0, y,-a2, 0,y+e, a2,section,section)
            draw_parallelepiped(0, y, a2,-b,y+e, 0,section,section)
            draw_parallelepiped(-b, y, 0,  0,y+e,-a2,section,section)
        else:
            draw_parallelepiped(0, y, a2, 0,y+e,-a2,section,section)
            draw_parallelepiped(-b, y, 0,  0,y+e, a2,section,section)
            draw_parallelepiped(0, y, -a2,-b,y+e, 0,section,section)
        # Barras verticales
        draw_parallelepiped(0,y,-a2,0,y+e,-a2,section,section)
        draw_parallelepiped(0,y,a2, 0,y+e,a2,section,section)
        draw_parallelepiped(-b,y, 0, -b,y+e,0,section,section)

        # Next level
        y=y+e
    # Barras horizontales
    draw_parallelepiped(0, y,-a2, 0, y, a2, section, section)
    draw_parallelepiped(0, y, a2, -b, y, 0, section, section)
    draw_parallelepiped(-b, y, 0,  0, y, -a2, section, section)

    glPopMatrix()


def draw_hook(height):
    skeleton = [
        [0.0, 0.0],
        [0.0, -0.3],
        [-0.3,-0.6],
        [0.0, -0.8],
        [0.2, -0.7]
    ]
    normal = [
        [1.0, 0.0],
        [0.89,0.45],
        [1.0, 0.0],
        [0.2, 0.98],
        [0.45, 0.89]
    ]
    N = 5 # Numero de puntos del skeleton
    thick=0.1

    for i in range(1, N):
        skeleton[i][0] *= height
        skeleton[i][1] *= height

    glShadeModel(GL_SMOOTH)

    glPushMatrix()

    for i in range(0, N-1):
        glBegin(GL_QUAD_STRIP)

        glNormal3f(normal[i][0], normal[i][1], 0.0)
        glVertex3f(skeleton[i][0]+thick, skeleton[i][1], 0)
        glNormal3f(normal[i+1][0], normal[i+1][1], 0.0)
        glVertex3f(skeleton[i+1][0]+thick, skeleton[i+1][1], 0)
        glNormal3f(0.0, normal[i][1], -normal[i][0])
        glVertex3f(skeleton[i][0], skeleton[i][1], -thick)
        glNormal3f(0.0, normal[i+1][1], -normal[i+1][0])
        glVertex3f(skeleton[i+1][0], skeleton[i+1][1], -thick)
        glNormal3f(-normal[i][0], normal[i][1], 0.0)
        glVertex3f(skeleton[i][0]-thick, skeleton[i][1], 0)
        glNormal3f(-normal[i+1][0], normal[i+1][1], 0.0)
        glVertex3f(skeleton[i+1][0]-thick, skeleton[i+1][1], 0)
        glNormal3f(0.0, normal[i][1], normal[i][0])
        glVertex3f(skeleton[i][0], skeleton[i][1], thick)
        glNormal3f(0.0, normal[i+1][1], normal[i+1][0])
        glVertex3f(skeleton[i+1][0], skeleton[i+1][1], thick)
        glNormal3f(normal[i][0], normal[i][1], 0.0)
        glVertex3f(skeleton[i][0]+thick, skeleton[i][1], 0)
        glNormal3f(normal[i+1][0], normal[i+1][1], 0.0)
        glVertex3f(skeleton[i+1][0]+thick, skeleton[i+1][1], 0)

        glEnd()

    glBegin(GL_TRIANGLE_FAN)

    i = N-1
    glNormal3f(normal[i][0],  normal[i][1], 0.0)
    glVertex3f(skeleton[i][0],  skeleton[i][1], 0)
    i = N-2
    glNormal3f(normal[i][0], normal[i][1], 0)
    glVertex3f(skeleton[i][0]+thick,  skeleton[i][1], 0)
    glNormal3f(0.0, normal[i][1], -normal[i][0])
    glVertex3f(skeleton[i][0],  skeleton[i][1], -thick)
    glNormal3f(-normal[i][0], normal[i][1], 0.0)
    glVertex3f(skeleton[i][0]-thick,  skeleton[i][1], 0)
    glNormal3f(0.0, normal[i][1], normal[i][0])
    glVertex3f(skeleton[i][0],  skeleton[i][1], thick)
    glNormal3f(normal[i][0], normal[i][1], 0.0)
    glVertex3f(skeleton[i][0]+thick,  skeleton[i][1], 0)

    glEnd()

    glPopMatrix()

    glShadeModel(GL_FLAT)

def draw_cilinder(h, r):
    glPushMatrix()

    glShadeModel(GL_SMOOTH)

    # Caras laterales
    glBegin(GL_QUAD_STRIP)
    glNormal3f(1.0, 0.0, -1.0)

    glVertex3f(r, h, -r)
    glVertex3f(r, 0, -r)

    glNormal3f(-1.0, 0.0, -1.0)

    glVertex3f(-r, h, -r)
    glVertex3f(-r, 0, -r)

    glNormal3f(-1.0, 0.0, 1.0)

    glVertex3f(-r, h, r)
    glVertex3f(-r, 0, r)

    glNormal3f(1.0, 0.0, 1.0)

    glVertex3f(r, h, r)
    glVertex3f(r, 0, r)

    glNormal3f(1.0, 0.0, -1.0)

    glVertex3f(r, h, -r)
    glVertex3f(r, 0, -r)
    glEnd()
    glShadeModel(GL_FLAT)
    # Tapas
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-r, h, -r)
    glVertex3f(-r, h, r)
    glVertex3f(r, h, r)
    glVertex3f(r, h, -r)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-r, 0, -r)
    glVertex3f(r, 0, -r)
    glVertex3f(r, 0, r)
    glVertex3f(-r, 0, r)
    glEnd()

    glPopMatrix()

def draw_tower(h, a, b, n, section=0.08):
    if n < 1:
        raise Exception("Numero de segmentos en torre menor que 1")

    y=0
    e=float(h)/float(n) # Altura entre dos niveles
    da = float(a) / (2.0*n)
    db = float(b) / (2.0*n)
    a2 = float(a) / 2.0
    b2 = float(b) / 2.0

    glPushMatrix()

    for i in range(0, n):
        # Barras horizontales
        draw_parallelepiped(-a2,y,-b2, a2,y,-b2,section, section)
        draw_parallelepiped(a2,y,-b2, a2,y, b2,section, section)
        draw_parallelepiped(a2,y, b2,-a2,y, b2,section, section)
        draw_parallelepiped(-a2,y, b2,-a2,y,-b2,section, section)

        # Barras oblicuas
        if i % 2:
            draw_parallelepiped(-a2,y,-b2, a2-da,y+e,-b2+db,section, section)
            draw_parallelepiped(a2,y,-b2, a2-da,y+e, b2-db,section, section)
            draw_parallelepiped(a2,y, b2,-a2+da,y+e, b2-db,section, section)
            draw_parallelepiped(-a2,y, b2,-a2+da,y+e,-b2+db,section, section)
        else:
            draw_parallelepiped(a2,y,-b2,-a2+da,y+e,-b2+db,section, section)
            draw_parallelepiped(a2,y, b2, a2-da,y+e,-b2+db,section, section)
            draw_parallelepiped(-a2,y, b2, a2-da,y+e, b2-db,section, section)
            draw_parallelepiped(-a2,y,-b2,-a2+da,y+e, b2-db,section, section)

        # Barras verticales
        draw_parallelepiped(-a2,y,-b2,-a2+da,y+e,-b2+db,section, section)
        draw_parallelepiped(a2,y,-b2, a2-da,y+e,-b2+db,section, section)
        draw_parallelepiped(-a2,y, b2,-a2+da,y+e, b2-db,section, section)
        draw_parallelepiped(a2,y, b2, a2-da,y+e, b2-db,section, section)

        # Next level
        y = y+e
        a2 = a2 - da
        b2 = b2 -db

    # Barras horizontales de terminacion
    draw_parallelepiped(-a2,y,-b2, a2,y,-b2,section, section)
    draw_parallelepiped(a2,y,-b2, a2,y, b2,section, section)
    draw_parallelepiped(a2,y, b2,-a2,y, b2,section, section)
    draw_parallelepiped(-a2,y, b2,-a2,y,-b2,section, section)

    glPopMatrix()
