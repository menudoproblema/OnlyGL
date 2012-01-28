from OpenGL.GL import *

from only.gl import colors
from only.gl import models

from primitives import *


########################################################################
##                                                                    ##
##                              Box                                   ##
##                                                                    ##
########################################################################


class Box(models.BoxModel):
    def __init__(self, *args, **kwargs):
        super(Box, self).__init__(*args, **kwargs)
        if self.color is None:
            self.color = colors.BROWN

    def model(self):
        draw_box(self.width, self.height, self.depth)


########################################################################
##                                                                    ##
##                            Building                                ##
##                                                                    ##
########################################################################


class Building(models.BoxModel):
    def __init__(self, *args, **kwargs):
        super(Building, self).__init__(*args, **kwargs)
        if self.color is None:
            self.color = colors.GRAY

    def model(self):
        draw_box(self.width, self.height, self.depth)


########################################################################
##                                                                    ##
##                             Crane                                  ##
##                                                                    ##
########################################################################


class CraneTower(models.BoxModel):
    def __init__(self, *args, **kwargs):
        super(CraneTower, self).__init__(*args, **kwargs)
        self._levels = int(self.height)

    def model(self):
        draw_tower(self.height, self.depth, self.width, self._levels)

class CraneBase(models.BoxModel):
    def model(self):
        draw_box(self.width, self.height, self.depth)

class CraneLeg(models.BoxModel):
    def __init__(self, *args, **kwargs):
        super(CraneLeg, self).__init__(*args, **kwargs)
        self._levels = int(self.height)

    def model(self):
        draw_framework(self.width, self.height, self.depth, self._levels)

class CraneCab(models.BoxModel):

    def _transfomations(self):
        glTranslatef(self.x, self.y, self.z)

    def model(self):
        draw_box(self.width, self.height, self.depth)

class CraneJib(models.Model):
    def __init__(self, length, width, rope_length=5.0,
                 rope_thick=0.05, rope_color=colors.BROWN,
                 hook_height=2.5, hook_color=colors.GRAY,
                 z_angle=0.0, **kwargs):
        super(CraneJib, self).__init__(**kwargs)
        # Jib properties
        self.length = length
        self.width = width
        self._jib_levels = int(length)
        self.z_angle = z_angle
        # Hook properties
        self.hook_height = hook_height
        self.hook_color = hook_color
        # Rope properties
        self.rope_length = rope_length
        self.rope_thick = rope_thick
        self.rope_color = rope_color

    def _transfomations(self):
        super(CraneJib, self)._transfomations()
        glRotatef(self.z_angle, 0.0, 0.0, 1.0)

    def model(self):
        # Pintamos el gancho y la cuerda
        glPushMatrix()
        glTranslatef(self.length, 0.0, 0.0)
        glRotatef(-self.z_angle, 0.0, 0.0, 1.0)
        glTranslatef(0.0, -self.rope_length, 0.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.rope_color)
        draw_cilinder(self.rope_length, self.rope_thick);
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.hook_color)
        draw_hook(self.hook_height)
        glPopMatrix()

        # Reestablecemos el color de la pluma
        if self._selected:
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, colors.HIGHLIGHT)
        elif self.color:
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)

        # Pintamos la pluma
        glPushMatrix()
        glRotatef(-90.0, 0.0, 0.0, 1.0);
        draw_jib(self.width, self.length, self._jib_levels)
        glPopMatrix()

class Crane(models.Model):
    def __init__(self, **kwargs):
        super(Crane, self).__init__(**kwargs)
        # Legs
        leg_width = kwargs.get('leg_width', 1.0)
        leg_height = kwargs.get('leg_height', 4.0)
        leg_depth = kwargs.get('leg_depth', 1.0)
        leg_color = kwargs.get('leg_color', colors.YELLOW)
        leg_mov = kwargs.get('leg_movement', 0.5)

        self.base = kwargs.get('base', CraneBase(6.0, 1.5, 6.0, color=colors.BROWN))
        self.cab = kwargs.get('cab', CraneCab(10.0, 3.0, 10.0, color=colors.ORANGE))
        self.jib = kwargs.get('jib', CraneJib(8.0, 1.5, color=colors.YELLOW))
        self.jib.x = kwargs.get('jib_movement', self.cab.width/2.0-0.2)
        self.tower = kwargs.get('tower', CraneTower(3.0, 6.0, 1.5, color=colors.YELLOW))

        # Calculating legs movements
        base_width2 = self.base.width / 2.0
        leg_width2 = leg_width / 2.0
        positive_movement = base_width2 - leg_width2 - leg_mov;
        negative_movement = -(base_width2) + leg_width2 + leg_mov;
        self.legs = (
            CraneLeg(
                leg_width, leg_height, leg_depth,
                x=negative_movement, z=negative_movement,
                color=leg_color
            ),
            CraneLeg(
                leg_width, leg_height, leg_depth,
                x=positive_movement, z=negative_movement,
                color=leg_color
            ),
            CraneLeg(
                leg_width, leg_height, leg_depth,
                x=negative_movement, z=positive_movement,
                color=leg_color
            ),
            CraneLeg(
                leg_width, leg_height, leg_depth,
                x=positive_movement, z=positive_movement,
                color=leg_color
            ),
        )

    def model(self):
        # Base
        for leg in self.legs:
            leg.draw()

        glTranslatef(0.0, self.legs[0].height, 0.0);
        self.base.draw()
        glTranslatef(0.0, self.base.height, 0.0)

        glRotatef(self.cab.y_angle, 0.0, 1.0, 0.0)
        self.cab.draw()
        glTranslatef(0.0, self.cab.height, 0.0)

        self.jib.draw()
        self.tower.draw()

        t1 = self.jib.length * math.sin(math.radians(self.jib.z_angle))
        height = self.jib.x + self.jib.length*math.cos(math.radians(self.jib.z_angle))
        t2 = self.tower.height - t1
        rope_lenght = math.sqrt(height*height + t2*t2)
        beta = math.degrees(math.acos(t2/rope_lenght))
        glTranslatef(0.0, self.tower.height, 0.0)
        glRotatef(beta, 0.0, 0.0, 1.0)
        glRotatef(180.0, 0.0, 0.0, 1.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,colors.BROWN)
        draw_cilinder(rope_lenght, self.jib.rope_thick)

    def set_selected(self, value):
        self._selected = value
        self.base._selected = value
        self.cab._selected = value

    def collision(self, obj, xyz=False):
        """Crane never collisions."""
        return False

