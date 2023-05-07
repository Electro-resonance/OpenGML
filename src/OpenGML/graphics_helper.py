# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 17th April 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Base class of helper functions for OpenGML graphics
# =============================================================================

import math
import trig_tables as trig
import numpy as np
from scipy.stats import norm
import scipy.spatial
from scipy.spatial import HalfspaceIntersection
import cdd as pcdd # Requires the pycddlib

class GraphicsHelperBaseClass(object):
    screen = None
    window = None
    canvas = None
    fbo = None
    screen_width = 10
    screen_height = 10
    BACKGROUND = [100, 100, 100, 100]
    sigma = 10
    sigma_constant = sigma * math.sqrt(2 * math.pi)
    image_cache = {}
    help_state = 2
    help_scaling = 100
    credits_request=False


    def init(self,window1):
        """
        Set up the global variable pointing to the Pygame screen
        """
        self.window = window1
        self.screen_width, self.screen_height = self.window.size
        self.image_cache = [None, None, None, None, None, None, None, None]


    def screen_get_screen_size(self):
        """
        Return screen size
        """
        return [self.screen_width, self.screen_height]


    def screen_get_mid_position(self):
        """
        Return screen midpoint
        """
        return [self.screen_width/2, self.screen_height/2]

    def add_canvas(self,canvas1, fbo1):
        self.canvas = canvas1
        self.fbo = fbo1


    def screen_clear(self):
        return None


    def get_pixel_colors(self,texture, dims):
        """
        Return an array of [rgba] for colours of the given texture
        """
        return None


    def get_pixel_color(self,colour_array, image_dims, pos):
        """
        Return the colour at a point in an array representing a photo
        """
        return (0,0,0,0)


    def grab_circular_photo_blit(self,im, colour_array, image_dims, image_scale, texture, x, y, w, h, transparent_colour, scale):
        """
        Grab an area from a photo
        """
        return [0, 0, 0, [0,0,0,255]]



    def add_canvas(self,canvas1, fbo1):
        return None


    def create_spiral_blit(self,pos, r, line_width, colour, transparent_colour, transparency, gears, phase, spiral_rate, spiral_mode, extra_angle):
        """
        Create blit with spiral
        """
        return [0, 0, 0]

    def create_circular_blit(self,pos, r, line_width, colour, transparent_colour, transparency, gears, phase):
        """
        Create blit with circle
        """
        return [0, 0, 0]

    def create_circle(self, cache_pointer, pos, diameter, line_width, colour, transparent_colour, transparency, gears, phase):
        """
        Create a circle
        """
        if (cache_pointer in self.image_cache.keys()):
            self.plot_centre_blit(self.image_cache[cache_pointer], pos)
        else:
            self.image_cache[cache_pointer] = self.create_circular_blit(
                pos, diameter, line_width, colour, transparent_colour, transparency, gears, phase)
        return

    def create_sphere(self, cache_pointer, pos, diameter, line_width, colour, transparent_colour, transparency, gears, phase):
        """
        Create a sphere
        """
        return

    def grab_circular_colour(self,image1, r):
        """
        Grab colour from the middle of an area
        """
        return 0,0,0


    def create_star_blit(self,pos, r, thickness, colour, transparent_colour, transparency):
        """
        Create blit with star
        create_star_blit(pos,100,5,[255,0,0],[0,0,0],1.0)
        """
        return [0,0,0]


    def plot_centre_blit(self,part, pos):
        """
        Plot an area after rotating preserving centre of the image
        """
        return [0,0,0]


    def plot_rotated_blit(self,part, pos, angle, ellipse_mask=False, transparency=1.0):
        """
        Plot an area after rotating
        """
        return [0,0,0]


    def plot_rotated_centre_blit(self,part, pos, angle, ellipse_mask=False, transpareny=1.0):
        """
        Plot an area after rotating preserving centre of the image
        """
        return [0,0,0]


    def plot_lines(self,line_points, colour, transparency, line_width, avg_height, screen=None, stipple=False, polygons=False, plot_mode=0):
        """
        Plot a 2D set of lines
        """
        return None

    def plot_lines_3d(self,line_points, colour, transparency, line_width=1.0, screen=None, stipple=False,polygons=False, edge_sequence=[]):
        """
        Plot a 3D set of lines
        """
        return None


    def plot_gaussian(self,x_offset, y_offset, height, colour, transparency, width,max_phases, raw_x_offset=0, xscale=600, screen=None):
        xy_plot = []
        x_axis_length=1000
        y_axis_length=350
        if (height == 360):
            x_axis = np.arange(0, 50, 1)  # +x_offset
        else:
            x_axis = np.arange(-50, 50, 1)  # +x_offset
        y_axis = norm.pdf(x_axis, 0, self.sigma)*self.sigma_constant*height+y_offset
        x_axis2 = x_axis+x_offset
        #xy_plot.extend((0, y_offset))
        for i in range(len(x_axis)):
            xy_plot.extend((x_axis2[i], y_axis[i]))
            x_test_pos=int(x_axis2[i] - raw_x_offset)
            if(y_axis[i]>max_phases[x_test_pos]):
                max_phases[x_test_pos]=y_axis[i]
        self.plot_lines(xy_plot, colour, transparency, width, screen=screen)
        if(height==360):
            xy_plot = []
            xy_plot.extend((x_axis_length, y_offset))
            xy_plot.extend((x_axis_length-5, y_offset-5))
            xy_plot.extend((x_axis_length, y_offset))
            xy_plot.extend((x_axis_length-5, y_offset+5))
            xy_plot.extend((x_axis_length, y_offset))
            xy_plot.extend((x_offset, y_offset))
            xy_plot.extend((x_offset, y_offset+y_axis_length))
            xy_plot.extend((x_offset-5, y_offset + y_axis_length -5))
            xy_plot.extend((x_offset, y_offset + y_axis_length))
            xy_plot.extend((x_offset + 5, y_offset + y_axis_length - 5))
            self.plot_lines(xy_plot, colour, 1.0, width, screen=screen)
        #print(xy_plot)
        return max_phases


    def calc_gaussian(self,freq, phase,max_phases):
        if (phase == 360):
            x_axis = np.arange(0, 50, 1)
        else:
            x_axis = np.arange(-50, 50, 1)
        y_axis = norm.pdf(x_axis, 0, 10)*phase * self.sigma_constant
        x_axis2 = x_axis+freq
        #xy_plot.extend((0, y_offset))
        for i in range(len(x_axis)):
            x_test_pos=int(x_axis2[i])
            if(y_axis[i]>max_phases[x_test_pos]):
                max_phases[x_test_pos]=y_axis[i]
        return max_phases

    def plot_max(self,x_offset, y_offset, height, colour, transparency, width,max_phases, raw_x_offset=0, xscale=600, screen=None):
        xy_plot = []
        x_count=x_offset
        for i in max_phases:
            xy_plot.extend((x_count, i))
            x_count+=1

        self.plot_lines(xy_plot, colour, transparency, width, screen)
        return max_phases


    def draw_singularity(self,cache_pointer0,cache_pointer1,mypos,mypos2,orbit_radius,phase,angle_offset,colour,draw_mode,is_spiral,spiral_rotates,spiral_mode,spiral_rate,max_r):
        if(draw_mode >= 2 and draw_mode < 7):
            if (cache_pointer0 in self.image_cache.keys()):
                if(is_spiral and spiral_rotates != 0):
                    self.plot_rotated_centre_blit(
                        self.image_cache[cache_pointer0], mypos2, phase*spiral_rotates)
                else:
                    self.plot_centre_blit(self.image_cache[cache_pointer0], mypos2)
            else:
                if(is_spiral):
                    self.image_cache[cache_pointer0] = self.create_spiral_blit(mypos2, orbit_radius, 2, colour, [
                                                             0, 0, 0], 200, False, phase, spiral_rate, spiral_mode, angle_offset)
                else:
                    self.image_cache[cache_pointer0] = self.create_circular_blit(
                        mypos2, orbit_radius, 2, colour, [0, 0, 0], 200, False, phase)
            self.create_sphere(cache_pointer0, mypos2, orbit_radius, 2, colour, [0, 0, 0], 200, False, phase)
        elif(draw_mode >= 7):
            self.create_circle(cache_pointer1, mypos, orbit_radius-max_r, 4,  colour, [0, 0, 0], 200, True, phase)

    def request_help(self,credits=False):
        """
        Reset the statemachine to initiate the help screen
        :return:
        """
        if(self.help_state>=2):
            self.credits_request=credits
            self.help_state = 0
            self.help_scaling = 100
            self.update_help_state()

    def run_help(self):
        """
        Prototype method to update the hep screen and listen for keyboard events
        :return: Returns when a key is pressed
        """
        return

    def help_display_text(self,help_scaling):
        """
        Prototype method to display the scaled help text
        """
        return

    def update_help_state(self):
        """
        Prototype method for state machine for help display
        :return:
        """
        return

    def key_pressed(self, keycode):
        """
        Prototype method to accept key presses from engine
        :return:
        """
        return