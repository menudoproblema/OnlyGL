#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from only.gl import colors
from only.gl.cameras import Camera
from only.gl.models import BoxModel
from only.gl.scene import Scene, GLUT_WHEEL_UP, GLUT_WHEEL_DOWN

from models import Crane, Box, Building
from primitives import draw_box


class EditorScene(Scene):
    NEUTRAL_STATE = 0
    MOVING_OBJECT_STATE = 1
    ADDING_CRANES_STATE = 2
    ADDING_BOXES_STATE = 3
    ADDING_BUILDINGS_STATE = 4

    def select_object(self, obj):
        """
        Selecciona un objeto de la escena y crea el menú contextual
        para mover el objeto.
        """
        # Deselecting the current selected object
        if self.selected_object is not None:
            self.deselect_object()
        # Selecting the new object
        self.selected_object = obj
        self.selected_object.set_selected(True)

    def deselect_object(self):
        """Deselecciona el objeto actualmente seleccionado."""
        # Deselecting the current selected object
        if self.selected_object is not None:
            self.selected_object.set_selected(False)
            self.selected_object = None

    def _set_collisionable_objects(self):
        self.collisionable = tuple(self.boxes + self.buildings)

    def add_crane(self, x, y, z):
        name = len(self.cranes)
        crane = Crane(name=name, x=x, y=y, z=z)
        self.cranes.append(crane)
        return crane

    def add_box(self, x, y, z, width, height, depth):
        name = len(self.boxes)
        box = Box(
            name=name,
            x=x, y=y, z=z,
            width=width, height=height, depth=depth
        )
        self.boxes.append(box)
        self._set_collisionable_objects()
        return box

    def add_building(self, x, y, z, width, height, depth):
        name = len(self.buildings)
        building = Building(
            name=name,
            x=x, y=y, z=z,
            width=width, height=height, depth=depth
        )
        self.buildings.append(building)
        self._set_collisionable_objects()
        return building

    def _go_up_collisionable(self, collisionable):
        y = 0.0
        # Calculating new height
        for obj in self.collisionable:
            if obj != collisionable:
                if collisionable.collision(obj):
                    # Which one is higher?
                    y = max(obj.y + obj.height, y)
        return y


    def menu_events(self, option):
        self.status = option
        return 0

    def init(self):
        super(EditorScene, self).init()
        self.menu = glutCreateMenu(self.menu_events)

        glutAddMenuEntry("Neutral", EditorScene.NEUTRAL_STATE)
        glutAddMenuEntry("Add crane", EditorScene.ADDING_CRANES_STATE)
        glutAddMenuEntry("Add box", EditorScene.ADDING_BOXES_STATE)
        glutAddMenuEntry("Add building", EditorScene.ADDING_BUILDINGS_STATE)

        glutAttachMenu(GLUT_RIGHT_BUTTON)

    def init_model(self):
        self.CRANE_NAME = 1
        self.BOX_NAME = 2
        self.BUILDING_NAME = 3

        self.cranes = [
            Crane(name=0, x=10, z=10),
            Crane(name=1, x=-15, z=-10),
        ]
        self.boxes = [
            Box(2.0, 2.0, 2.0, name=0, x=12, z=-8),
            Box(2.0, 2.0, 2.0, name=1, x=-15, z=-15),
            Box(2.0, 2.0, 2.0, name=2, x=12, z=8),
        ]
        self.buildings = [
        ]

        self._set_collisionable_objects()

        self.status = EditorScene.NEUTRAL_STATE
        self.selected_object = None

    def draw(self):
        glPushName(self.CRANE_NAME)
        for crane in self.cranes:
            crane.draw()
        glPopName()

        glPushName(self.BOX_NAME)
        for box in self.boxes:
            box.draw()
        glPopName()

        glPushName(self.BUILDING_NAME)
        for building in self.buildings:
            building.draw()
        glPopName()

        # Draw the floor
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, colors.GREEN)
        glTranslatef(0.0, -0.5, 0.0)
        draw_box(200.0, 0.5, 200.0)

    def animationfunc(self, value):
        glutPostRedisplay()
        glutTimerFunc(250, self.animationfunc, 0)

    def mousefunc(self, button, state, x, y):
        super(EditorScene, self).mousefunc(button, state, x, y)

        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.mouse_state.pressed = False
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.mouse_state.pressed = True

        if self.status == EditorScene.NEUTRAL_STATE:
            """Neutral state"""
            if self.mouse_state.pressed:
                # Looking for a object
                hit = self.pick(x, y)
                if not hit or len(hit) != 2:
                    self.deselect_object()
                    return # Nothing interesting
                # Which one?
                model, name = hit
                if model == self.CRANE_NAME:
                    self.status = EditorScene.MOVING_OBJECT_STATE
                    self.select_object(self.cranes[name])
                elif model == self.BOX_NAME:
                    self.status = EditorScene.MOVING_OBJECT_STATE
                    self.select_object(self.boxes[name])
                elif model == self.BUILDING_NAME:
                    self.status = EditorScene.MOVING_OBJECT_STATE
                    self.select_object(self.buildings[name])
                else:
                    self.deselect_object()

                if self.selected_object:
                    glutSetCursor(GLUT_CURSOR_NONE)
        elif self.status == EditorScene.MOVING_OBJECT_STATE:
            """Moving object state"""
            if not self.mouse_state.pressed:
                self.status = EditorScene.NEUTRAL_STATE
                glutSetCursor(GLUT_CURSOR_LEFT_ARROW)
        elif self.status == EditorScene.ADDING_CRANES_STATE:
            """Adding cranes state"""
            if self.mouse_state.pressed:
                real_x, real_y, real_z = self.get_world_coordinates(x, y)
                crane = self.add_crane(real_x, 0.0, real_z)
                self.select_object(crane)
                glutSetCursor(GLUT_CURSOR_NONE)
            elif not self.mouse_state.pressed:
                glutSetCursor(GLUT_CURSOR_LEFT_ARROW)
        elif self.status == EditorScene.ADDING_BOXES_STATE:
            """Adding boxes state"""
            if self.mouse_state.pressed:
                real_x, real_y, real_z = self.get_world_coordinates(x, y)
                box = self.add_box(real_x, 0.0, real_z, 2.0, 2.0, 2.0)
                box.y = self._go_up_collisionable(box)
                self.select_object(box)
                glutSetCursor(GLUT_CURSOR_NONE)
            elif not self.mouse_state.pressed:
                glutSetCursor(GLUT_CURSOR_LEFT_ARROW)
        elif self.status == EditorScene.ADDING_BUILDINGS_STATE:
            """Adding buildings state"""
            if self.mouse_state.pressed:
                real_x, real_y, real_z = self.get_world_coordinates(x, y)
                building = self.add_building(real_x, 0.0, real_z, 25.0, 40.0, 30.0)
                self.select_object(building)
                glutSetCursor(GLUT_CURSOR_NONE)
            elif not self.mouse_state.pressed:
                glutSetCursor(GLUT_CURSOR_LEFT_ARROW)

    def motionfunc(self, x, y):
        def update_motion():
            # Updating the movement
            self.mouse_state.x = x
            self.mouse_state.y = y
            glutPostRedisplay()

        if self.status == EditorScene.NEUTRAL_STATE:
            x_shift = 0.1*(x-self.mouse_state.x)
            y_shift = 0.1*(y-self.mouse_state.y)
            self._yrot = self._yrot + x_shift
            self._xrot = self._xrot + y_shift
        elif self.status == EditorScene.MOVING_OBJECT_STATE or \
           self.status == EditorScene.ADDING_BOXES_STATE:
            # Not selected?
            if self.selected_object is None:
                self.status == EditorScene.NEUTRAL_STATE
                update_motion()
                return

            x_shift = 0.1*(x-self.mouse_state.x)
            z_shift = 0.1*(y-self.mouse_state.y)
            if not self.selected_object in self.collisionable:
                # Move the object
                self.selected_object.x += x_shift
                self.selected_object.z += z_shift
                update_motion()
                return
            # Copy the selected object
            prev_obj = BoxModel(
                x=self.selected_object.x,
                y=self.selected_object.y,
                z=self.selected_object.z,
                width=self.selected_object.width,
                height=self.selected_object.height,
                depth=self.selected_object.depth
            )
            # Move the object
            self.selected_object.x += x_shift
            self.selected_object.z += z_shift

            go_up = True
            for obj in self.collisionable:
                if obj != self.selected_object:
                    # Habia colision y 'obj' esta arriba
                    if prev_obj.collision(obj) and obj.y > prev_obj.y:
                        # Comprobamos si no colisiona con el objeto movido
                        if not self.selected_object.collision(obj):
                            # Bajamos el objeto
                            obj.y -= self.selected_object.height
                        else:
                            go_up = False

            if go_up:
                self.selected_object.y = self._go_up_collisionable(
                    self.selected_object)


        update_motion()

    def keyboardfunc(self, *args):
        super(EditorScene, self).keyboardfunc(*args)


def main():
    glutInit(sys.argv)

    scene = EditorScene()

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(scene.viewport.width, scene.viewport.height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("City editor - OnlyGL")

    scene.init()

    glutDisplayFunc(scene.displayfunc)
    glutReshapeFunc(scene.reshapefunc)
    glutTimerFunc(200, scene.animationfunc, 0)
    glutKeyboardFunc(scene.keyboardfunc)
    glutMouseFunc(scene.mousefunc)
    glutMotionFunc(scene.motionfunc)

    glutMainLoop()


print "Hit ESC key to quit."
main()
