# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 17th April 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Graphics abstraction layer for variant of OpenGML using
# 2D graphics implemented with Kivy applications Engine
# =============================================================================

import os as _os
_ENVIRONMENT_VAR_NAME = "PYGAME_HIDE_SUPPORT_PROMPT"
_ADD_VAR = _ENVIRONMENT_VAR_NAME not in _os.environ
if _ADD_VAR:
    _os.environ[_ENVIRONMENT_VAR_NAME] = "Added by OpenGML"


import sys
sys.path.append("../../src/OpenGML") #AddOpenGML path

from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window
from kivy.clock import Clock
from gl_text_drawing import *

from threading import Thread
from time import sleep

from Sonic_GML import *
from GML import *
from graphics_helper import *
from blit_functions import *
from colour_functions import * #RGB definitions of Colours

from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

class GML_App_2D(App):

    def __init__(self,title="OpenGML",populate_callback=None,sonic_enabled=False,**kwargs):
        """
        Initialise by creating the GML tree
        """
        super(GML_App_2D, self).__init__(**kwargs)
        GML_graphics_helper().init(Window)
        GML_resize()
        GML_init()

        self.sonic_enabled=sonic_enabled
        self.set_title(title)
        self.FPS = 50 # Frames per second setting
        self.display=(800,800)
        self.populate(populate_callback)
        #Start on demo 0
        self.demo_select = 0
        self.rootNode = self.populate_function(self.demo_select)
        self.balance_phases=False
        self.mode_2d=1
        self.relative_zoom=0
        self.depth_projection=False
        self.callback_keys=[]
        self.x = 100
        self.y = 100
        self.button1 = None
        self.text1 = None
        self.fbo = None
        self.pause = True
        self.running_speed = 1
        self.sonic = None
        self.sonic_thread = None
        self.timer_loop = 0
        self.timer_max = 25
        self.run_on = True
        self.tempo = 1
        self.redraw=False
        self.demo_num_callback=None
        GML_graphics_helper().key_pressed('h') #Trigger help menu
        self.key_callback=None
        self.last_key_press=Clock.get_time()
        self.dt_key_press=0
        self.runtime_callback=None

    def on_window_resize(self, window, width, height):
        """
        Allow dynamic window resizes and redraw the GML tree
        to fit the new window size
        """
        print("width", width)
        print("height", height)
        self.rootNode.graphics_helper.init(Window)
        GML_resize()
        self.redraw = True

    def button_callback(self, value):
        """
        Mouse button callback
        """
        #Cycle the demo if the mouse button is pressed
        self.demo_select += 1
        if(self.demo_select > 14):
            self.demo_select = 0
        self.redraw = True

    def on_stop(self):
        if (self.sonic_thread is not None):
            self.playing_sounds = False
            self.sonic_thread.join()

    def set_title(self,title="OpenGML"):
        self.title=title
        Window.set_title(title)

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
            self.tempo= 1 / speed

    def balancing_phases(self,enable=True):
        self.balance_phases=enable

    def set_graphics_mode(self, mode=1):
        self.mode_3d = mode

    def set_zoom_relative(self,zoom=0):
        self.relative_zoom=zoom

    def set_depth_projection(self,depth_enable):
        self.depth_projection=depth_enable

    def add_key_callback(self,key,callback,redraw):
        self.callback_keys.append([key,callback,redraw])

    def add_demo_num_callback(self,demo_num_callback):
        self.demo_num_callback=demo_num_callback

    def add_key_callback(self,key_callback):
        self.key_callback=key_callback

    def add_runtime_callback(self,runtime_callback):
        self.runtime_callback = runtime_callback

    def build(self):
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_interval(self.update, 0.01 / 60.0)
        return self.update(0.0)

    def run2d(self):
        """
        Pass the screen object to the GML libraries
        """
        GML_graphics_helper().init(Window)
        GML_resize()
        GML_init()
        if(self.sonic_enabled==True):
            Sonic_GML_init()

        # Create the GML tree
        self.rootNode = self.populate_function(self.demo_select)

        self.rootNode.set_draw_mode(4)
        #Allow the GML singularities to rotate on redraw
        #self.rootNode.set_pause(False)
        self.fbo=Fbo(size=Window.size, with_stencilbuffer=True)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, None)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        if (self.sonic_enabled == True):
            self.sonic_thread = Thread(target=self.thread_sonic_player, args=(1,))
            self.sonic_thread.start()
            self.sonic = Sonic_GML()

        #Clock.schedule_interval(self.update, 0.01 / 60.0)
        #self.update(0.0)
        self.run()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        self.redraw = False

        current_time = Clock.get_time()
        self.dt_key_press = current_time - self.last_key_press
        self.last_key_press = current_time

        #if keycode[1] == 'k':
        #    glTranslatef(0, 0, 0.1)
        #if keycode[1] == 'm':
        #    glTranslatef(0, 0, -0.1)
        #if keycode[1] == 'j':
        #    glTranslatef(0, 0.03, 0)
        #if keycode[1] == 'n':
        #    glTranslatef(0, -0.03, 0)
        #if keycode[1] == 'o':
        #    glTranslatef(-0.03, 0, 0)
        #if keycode[1] == 'p':
        #    glTranslatef(0.03, 0, 0)

        #Key 'z' or the spacebar cycles through the demos
        if (keycode[1] == 'z' or keycode[0] == 32):
            self.demo_select += 1
            if(self.demo_select > 14):
                self.demo_select = 0
            self.redraw = True

        elif keycode[1] == 'd':
            self.pause=not(self.pause)
            self.rootNode.set_pause(self.pause)
            if(self.pause==True):
                self.running_speed=self.rootNode.oscillator_speed
                self.rootNode.set_oscillator_speed(0)
            else:
                self.rootNode.set_oscillator_speed(self.running_speed)

        elif keycode[1] == 'a':
            s1=self.rootNode.smallest_childs_parent()
            s11 = self.rootNode.smallest_child(7)
            if(len(self.rootNode.children1)<7):
                self.rootNode.add_singularity(0, diameter=8, freq=30 * 5, colour=[0, 255, 255])
            else:
                s2 = s11.add_singularity(0, diameter=8, freq=30 * 1.5, colour=[255, 255, 0])
            #s2=s11.add_singularity(0,diameter=8, freq=30 * 5, colour=[0,255,255])
            #s1[0].add_pentagon(0, diameter=6, freq=30 * 2,colour=[0,255,255])

        elif keycode[1] =='g':
            self.mode_2d += 1
            if (self.mode_2d > 4):
                self.mode_2d = 0
            print("2D mode:", self.mode_2d)

        elif keycode[1] == 'f':
            self.rootNode.balance_phases()

        elif keycode[1] == 's':
            self.rootNode.decrement()

        elif keycode[1] == '1':
            self.rootNode.increment_draw_mode(1, self.rootNode)
            if (self.sonic_enabled == True):
                self.sonic.increment_draw_mode(1, self.rootNode)
        elif keycode[1] == '2':
            if (self.sonic_enabled == True):
                self.sonic.increment_gml_mode(1)

        elif keycode[1] == '3':
            if (self.sonic_enabled == True):
                self.sonic.increment_chord_size(+1)
        elif keycode[1] == '4':
            if (self.sonic_enabled == True):
                self.sonic.increment_chord_size(-1)

        elif keycode[1] == '5':
            if (self.sonic_enabled == True):
                self.sonic.increment_octaves(+1)
        elif keycode[1] == '6':
            if (self.sonic_enabled == True):
                self.sonic.increment_octaves(-1)

        elif keycode[1] == '7':
            self.tempo += 1
        elif keycode[1] == '8':
            self.tempo -= 1

        GML_graphics_helper().key_pressed(keycode[1])
        if(self.key_callback is not None):
            self.key_callback(keycode[1],self.dt_key_press)

        if (self.redraw == True):
            # Create the GML tree
            self.rootNode = self.populate_function(self.demo_select)
            self.rootNode.print_tree()

        return True

    def update(self,dt):
        """
        Animate the GML tree and update the text
        """
        if(self.button1==None):
            self.button1=Button(text="Main button")
            self.button1.bind(on_press=self.button_callback)
            #Set up frame buffering on first iteration
            GML_graphics_helper().add_canvas(self.button1.canvas,self.fbo)

        if(GML_graphics_helper().update_help_state()==False):
            return self.button1

        # Clear on subsequent for replotting of updated GML trees
        self.button1.canvas.clear()

        if(self.redraw == True):
            self.rootNode = self.populate_function(self.demo_select)
            self.rootNode.print_tree()
            #Print the GML geometry as text
            print("GML geometry text representation: ",
                  self.rootNode.gml_to_text(100))
            self.redraw = False

        #Redraw the tree with phase rotations
        self.rootNode.run1(20) #Animate the GML

        if(self.sonic_enabled==True):
            self.sonic.circle_notes()
            self.rootNode.set_oscillator_speed(self.tempo / 10)

        if (self.mode_2d == 1):
            self.rootNode.gml_line_plot(100,polygons=True)
        if (self.mode_2d == 2):
            self.rootNode.gml_line_plot(100,polygons=True, plot_mode=1)  # Add lines
        if (self.mode_2d == 3):
            self.rootNode.gml_line_plot(100,polygons=False)
        if (self.mode_2d == 4):
            self.rootNode.gml_line_plot(100,polygons=False, plot_mode=1)  # Add lines

        if(self.demo_num_callback is not None):
            self.demo_num_callback(self, self.demo_select)

        if (self.balance_phases == True):
            self.rootNode.balance_phases()

        if (self.depth_projection == True):
            #Plot sidebars showing depth of the GML tree on X and y axes
            #Show a tree up to 20 deep
            for depth in range(1,20):
                self.rootNode.depth_projection(depth,[0,255,0],depth*10,True)
                self.rootNode.depth_projection(depth,[255,0,0],depth*10,False)


        if(self.text1==None):
            self.text1=FreeDrawText()
        self.text1.drawText(self.button1.canvas,40,70,"Defined Clocks: "+str(self.rootNode.oscillators()),24)
        self.text1.drawText(self.button1.canvas,40,100,"Dimensions: "+str(self.rootNode.dimensions()),24)
        if (self.sonic_enabled == True):
            self.text1.drawText(self.button1.canvas, 40, 450,"Tempo: "+str(int(self.tempo)), 18)
            self.sonic.drawText(self.text1, self.button1.canvas, 470, x=40)

        if(self.runtime_callback is not None):
            self.runtime_callback(self.rootNode)

        return self.button1

    def thread_sonic_player(self, name):
        logging.info("[Sonic Thread] Starting Sonification")
        self.playing_sounds = True
        while(self.playing_sounds):
            self.timer_loop += 1
            if(self.timer_loop >= self.timer_max):
                self.timer_loop = 0
                #print(self.timer_loop)
                if(self.run_on == True):
                    self.sonic.play_sonic_sequence(self.rootNode,sequence=True)
            sleep(0.01)
        logging.info("[Sonic Thread] Stopping Sonification")