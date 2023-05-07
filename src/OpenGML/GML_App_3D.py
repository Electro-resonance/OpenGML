# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 17th April 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Graphics abstraction layer for variant of OpenGML using
# 3D graphics implemented with OpenGL and PyGame applications Engine
# =============================================================================

import sys
sys.path.append("../../src/OpenGML") #AddOpenGML path

import os as _os
_ENVIRONMENT_VAR_NAME = "PYGAME_HIDE_SUPPORT_PROMPT"
_ADD_VAR = _ENVIRONMENT_VAR_NAME not in _os.environ
if _ADD_VAR:
    _os.environ[_ENVIRONMENT_VAR_NAME] = "Added by OpenGML"


from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from threading import Thread
from time import sleep

from Sonic_GML import *
from GML_3D import *


class GML_App_3D():

    def __init__(self,title="OpenGML",populate_callback=None,sonic_enabled=False,plan_mode=1):
        pygame.init()
        self.sonic_enabled=sonic_enabled
        self.set_title(title)
        self.FPS = 50 # Frames per second setting
        self.display=(800,800)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL |RESIZABLE)
        self.fpsClock = pygame.time.Clock()
        self.sysfont = pygame.font.get_default_font()
        #print('system font :', self.sysfont)
        self.plan_mode=plan_mode
        self.init_opengl()
        self.populate(populate_callback)
        #Start on demo 0
        self.demo_select = 0
        self.rootNode = self.populate_function(self.demo_select)
        self.balance_phases=False
        self.mode_3d=1
        self.plan_mode=1
        self.relative_zoom=0
        self.depth_projection=False
        self.callback_keys=[]
        self.sonic = None
        self.sonic_thread = None
        self.timer_loop = 0
        self.timer_max = 25
        self.run_on = True
        self.tempo = 1

    def set_title(self,title="OpenGML"):
        pygame.display.set_caption(title)

    def init_opengl(self):
        glEnable(GL_BLEND)
        #glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

        if(self.plan_mode == 1):
            #normal mode
            gluLookAt(5, 0, 0, -40, -35, 35, 0,0, 1)
        if (self.plan_mode == 2):
            #plan mode
            gluLookAt(0, -10, 0, 3, 0, +2, 0, 0, 1)
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    def populate(self,populate_function):
        self.populate_function=populate_function

    def initial_rotation_speed(self,speed):
        if(speed==0):
            self.running_speed = self.rootNode.oscillator_speed
            self.rootNode.set_oscillator_speed(0)
            self.rootNode.set_pause(True)
        else:
            self.rootNode.set_oscillator_speed(speed)
            self.rootNode.set_pause(False)
            self.tempo = 1 / speed

    def balancing_phases(self,enable=True):
        self.balance_phases=enable

    def set_graphics_mode(self, mode=1):
        self.mode_3d = mode

    def set_zoom_relative(self,zoom=0):
        self.relative_zoom=zoom
        glTranslatef(zoom,0,0)

    def set_depth_projection(self,depth_enable):
        self.depth_projection=depth_enable

    def add_key_callback(self,key,callback,redraw):
        self.callback_keys.append([key,callback,redraw])

    def run(self):
        """
        Pass the screen object to the GML libraries
        """
        GML_Use_PyGame()
        GML_graphics_helper().init(self.screen)
        GML_resize()
        GML_init()
        if(self.sonic_enabled==True):
            Sonic_GML_init()

        GML_graphics_helper().request_help()

        # Create the GML tree
        self.rootNode = self.populate_function(self.demo_select)

        self.rootNode.set_draw_mode(4)
        # Allow the GML singularities to rotate on redraw
        #self.rootNode.set_pause(False)
        self.pause = True
        self.running_speed = 1

        mode_change=pygame.time.get_ticks()

        self.displayCenter = [self.display[0]/2,self.display[1]/2]
        self.mouseMove = [0, 0]

        if (self.sonic_enabled == True):
            self.sonic_thread = Thread(target=self.thread_sonic_player, args=(1,))
            self.sonic_thread.start()
            self.sonic = Sonic_GML()

        done = False
        while not done:
            self.fpsClock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.VIDEORESIZE:
                    self.display=(event.w, event.h)
                    self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL | RESIZABLE)

            self.redraw=False
            keypress = pygame.key.get_pressed()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            glEnable(GL_DEPTH_TEST)

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()

            gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            # Key 'z' or the spacebar cycles through the demos
            if (keypress[pygame.K_z] or keypress[pygame.K_SPACE]):
                self.demo_select += 1
                if (self.demo_select > 14):
                    self.demo_select = 0
                self.redraw = True

            # apply any movment
            elif keypress[pygame.K_k]:
                glTranslatef(0,0,0.1)
            elif keypress[pygame.K_m]:
                glTranslatef(0,0,-0.1)
            elif keypress[pygame.K_j]:
                glTranslatef(0,0.03,0)
            elif keypress[pygame.K_n]:
                glTranslatef(0,-0.03,0)
            elif keypress[pygame.K_o]:
                glTranslatef(-0.03,0,0)
            elif keypress[pygame.K_p]:
                glTranslatef(0.03,0,0)

            elif (self.relative_zoom != 0):
                glTranslatef(0, 0, self.relative_zoom)
                self.relative_zoom=0

            elif keypress[pygame.K_d]:
                if((pygame.time.get_ticks()-mode_change)>80):
                    self.pause = not (self.pause)
                    if (self.pause == True):
                        self.running_speed = self.rootNode.oscillator_speed
                        self.rootNode.set_oscillator_speed(0)
                    else:
                        self.rootNode.set_oscillator_speed(self.running_speed)
                    self.rootNode.set_pause(self.pause)
                mode_change = pygame.time.get_ticks()

            elif keypress[pygame.K_a]:
                if((pygame.time.get_ticks()-mode_change)>80):
                    s1 = self.rootNode.smallest_childs_parent()
                    s11 = self.rootNode.smallest_child(7)
                    if (self.rootNode.mode_3d==False):
                        phase_offset=0
                        freq=30 * 1.5
                    else:
                        phase_offset=[0,0]
                        freq = [30 * 1.5, 30 * 1.5]
                    if (len(self.rootNode.children1) < 7):
                        self.rootNode.add_singularity(phase_offset, diameter=8, freq=freq, colour=[0, 255, 255])
                    else:
                        s2 = s11.add_singularity(phase_offset, diameter=8, freq=freq, colour=[255, 255, 0])
                    mode_change = pygame.time.get_ticks()

            elif keypress[pygame.K_g]:
                if ((pygame.time.get_ticks() - mode_change) > 80):
                    self.mode_3d+=1
                    if (self.mode_3d > 4):
                        self.mode_3d=0
                    print("3D mode:", self.mode_3d)
                    mode_change = pygame.time.get_ticks()

            elif keypress[pygame.K_f]:
                self.rootNode.balance_phases()

            elif keypress[pygame.K_s]:
                if ((pygame.time.get_ticks() - mode_change) > 50):
                    self.rootNode.decrement()
                    mode_change = pygame.time.get_ticks()

            elif keypress[pygame.K_h]:
                if ((pygame.time.get_ticks() - mode_change) > 50):
                    pygame.time.wait(100)
                    GML_graphics_helper().request_help()
                    pygame.time.wait(100)

            elif keypress[pygame.K_y]:
                if ((pygame.time.get_ticks() - mode_change) > 50):
                    pygame.time.wait(100)
                    GML_graphics_helper().request_help(credits=True)
                    pygame.time.wait(100)

            elif keypress[pygame.K_1]:
                self.rootNode.increment_draw_mode(1, self.rootNode)
                if (self.sonic_enabled == True):
                    self.sonic.increment_draw_mode(1, self.rootNode)
            elif keypress[pygame.K_2]:
                if (self.sonic_enabled == True):
                    self.sonic.increment_gml_mode(1)
            elif keypress[pygame.K_3]:
                if (self.sonic_enabled == True):
                    self.sonic.increment_chord_size(+1)
            elif keypress[pygame.K_4]:
                if (self.sonic_enabled == True):
                    self.sonic.increment_chord_size(-1)
            elif keypress[pygame.K_5]:
                if (self.sonic_enabled == True):
                    self.sonic.increment_octaves(+1)
            elif keypress[pygame.K_6]:
                if (self.sonic_enabled == True):
                    self.sonic.increment_octaves(-1)
            elif keypress[pygame.K_7]:
                self.tempo += 1
            elif keypress[pygame.K_8]:
                self.tempo -= 1

            for [key,callback,redraw] in self.callback_keys:
                if keypress[key]:
                    if ((pygame.time.get_ticks() - mode_change) > 80):
                        callback(key)
                        if(redraw):
                            self.redraw=True
                        mode_change = pygame.time.get_ticks()

            if(self.redraw==True):
                # Create the GML tree
                self.rootNode = self.populate_function(self.demo_select)
                self.rootNode.print_tree()

            # multiply the current matrix by the get the new view matrix and store the final view matrix
            glMultMatrixf(self.viewMatrix)
            self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            if(self.mode_3d == 1):
                self.rootNode.gml_line_plot(100, polygons=True) # Add lines
            if (self.mode_3d == 2):
                self.rootNode.gml_line_plot(100, polygons=True, plot_mode=1)  # Add lines
            if (self.mode_3d == 3):
                self.rootNode.gml_line_plot(100, polygons=False)  #Points
            if (self.mode_3d == 4):
                self.rootNode.gml_line_plot(100, polygons=False, plot_mode=1)  #Points


            self.rootNode.run1(100) #Animate the GML

            GML_graphics_helper().drawText(10, 10, "Defined Clocks: " + str(self.rootNode.oscillators()), 16)
            GML_graphics_helper().drawText(10, 30, "Dimensions: " + str(self.rootNode.dimensions()), 16)

            if (self.sonic_enabled == True):
                GML_graphics_helper().drawText(10, 50, "Tempo: " + str(self.tempo), 16)
                self.sonic.circle_notes()
                self.rootNode.set_oscillator_speed(self.tempo / 10)

            if(self.balance_phases==True):
                self.rootNode.balance_phases()

            if (self.depth_projection == True):
                for depth in range(1, 20):
                    self.rootNode.depth_projection(depth, [0, 255, 0], depth * 10, True)
                    self.rootNode.depth_projection(depth, [255, 0, 0], depth * 10, False)

            pygame.display.flip()

        pygame.quit()
        if (self.sonic_thread is not None):
            self.playing_sounds = False
            self.sonic_thread.join()
        exit()



    def thread_sonic_player(self, name):
        logging.info("[Sonic Thread] Starting Sonification")
        self.playing_sounds = True
        while (self.playing_sounds):
            self.timer_loop += 1
            if (self.timer_loop >= self.timer_max):
                self.timer_loop = 0
                # print(self.timer_loop)
                if (self.run_on == True):
                    self.sonic.play_sonic_sequence(self.rootNode, sequence=True)
            sleep(0.01)
        logging.info("[Sonic Thread] Stopping Sonification")