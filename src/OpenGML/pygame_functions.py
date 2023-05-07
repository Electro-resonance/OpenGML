# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 17th June 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Helper functions for 2D blit objects with Kivy
# =============================================================================

import math
import trig_tables as trig

import numpy as np
from graphics_helper import GraphicsHelperBaseClass
from polytopic_geometry import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import *
from PIL import Image
import numpy

import menu_functions as help_menu_text

class PygameGraphicsHelper(GraphicsHelperBaseClass):

    def init(self,window1):
        """
        Set up the global variable pointing to the Pygame screen
        """
        self.window = window1
        self.screen_width= self.window.get_width()
        self.screen_height= self.window.get_height()
        self.yRotated = 0
        #self.screen_width, self.screen_height = self.screen_get_screen_size()
        self.texture=0
        #self.data[256][256][3]=[][][]
        #self.data=np.empty([256,256,3], dtype=int)
        self.data = np.empty([256,256,3], dtype=np.int)
        self.make_texture()

    def add_canvas(self,canvas1, fbo1):
        """
        Add the canvas and framebuffer
        """
        self.canvas = canvas1
        self.fbo = fbo1

    def screen_clear(self):
        """
        Clear the screen
        """
        self.canvas.clear()
        #screen.fill([0,0,0])

    def make_texture(self):
        """
        Create a 3D texture for spheres
        """
        for y in range(0,255):
            for x in range(0,255):
                self.data[y][x][0]=np.random.randint(0,255)
                self.data[y][x][1]=np.random.randint(0,255)
                self.data[y][x][2]=np.random.randint(0,255)

        textures= glGenTextures(3)
        self.texture=int(textures[0])
        glGenTextures(0, self.texture)
        glBindTexture(GL_TEXTURE_3D, self.texture)
        glTexImage3D(GL_TEXTURE_3D, 0, GL_RGB, 256, 256, 1, 0, GL_RGB, GL_UNSIGNED_BYTE, self.data)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    def get_pixel_colors(self,texture, dims):
        """
        Return an array of [rgba] for colours of the given texture
        """
        return None


    def get_pixel_color(self,colour_array, image_dims, pos):
        """
        Return the colour at a point in an array representing a photo
        """
        return None


    def grab_circular_photo_blit(self,im, colour_array, image_dims, image_scale, texture, x, y, w, h, transparent_colour, scale):
        """
        Grab an area from a photo
        """
        return None

    def create_spiral_blit(self,pos, r, line_width, colour, transparent_colour, transparency, gears, phase, spiral_rate, spiral_mode, extra_angle):
        """
        Create blit with spiral
        """
        return None

    def create_circular_blit(self,pos, r, line_width, colour, transparent_colour, transparency, gears, phase):
        """
        Create blit with circle
        """
        #self.create_sphere(0, [pos,0,0], r, line_width, colour, transparent_colour, transparency, gears, phase)
        return

    def create_circle(self,cache_pointer, pos, r, line_width, colour, transparent_colour, transparency, gears, phase):
        """
        Redirect circle creation to a sphere
        """
        self.create_sphere(0, pos, r, line_width, colour, transparent_colour, transparency, gears, phase)

    def create_sphere(self,cache_pointer, pos, r, line_width, colour, transparent_colour, transparency, gears, phase):
        """
        Create a sphere
        """
        # glPushMatrix()
        # glTranslate(-1, (pos[0]*2 - 400) / 25 + 30, (pos[1]*2 - 400) / 256)
        # glColor4f(colour[0]*255, colour[1]*255, colour[2]*255, 1)
        # sphere = gluNewQuadric()
        # gluSphere(sphere, r * 1  / 256, 32, 16)  # Draw sphere
        # glPopMatrix()

        glPushMatrix()
        #glEnable(GL_TEXTURE_2D);

        mult = 2
        #glTranslate((pos[0]*2 - 400), (pos[1]*2 - 400),-1)
        #glTranslate((pos[0]*2 - 400) / 256, (pos[0]*2 - 400) / 256 /500, (pos[1]*2 - 400) / 256)
        glTranslate((pos[0] * 2) / 256, (pos[2] * 2 - 400) / 256, (pos[1] * 2 - 400) / 256)
        glColor4f(colour[0]*255, colour[1]*255*pos[1], colour[2]*255, 0.01)

        #glRotatef(self.yRotated+phase, self.yRotated, 1.0, 0.0);

        sphere = gluNewQuadric()
        sphere1 = gluNewQuadric()
        #gluQuadricDrawStyle(sphere, GLU_FILL);
        #gluQuadricTexture(sphere, GL_TRUE);
        gluQuadricNormals(sphere, GLU_SMOOTH);
        gluQuadricNormals(sphere1, GLU_FILL);

        #glRotatef(self.yRotated, self.yRotated, 1.0, 0.0);
        gluSphere(sphere, r * 2 / 256,31, 43)  # Draw sphere

        glColor4f(colour[0] * 255, colour[1] * 255 * pos[1], colour[2] * 255, 0.5)
        gluSphere(sphere1, r * 2 / 256+0.014, 30, 47)  # Draw sphere

        gluDeleteQuadric(sphere);
        gluDeleteQuadric(sphere1);
        glDisable(GL_TEXTURE_2D);

        #self.yRotated += np.random.randint(-100,100)/100000.0;

        glPopMatrix()

        return None

    def grab_circular_colour(self,image1, r):
        """
        Grab colour from the middle of an area
        """
        return None


    def create_star_blit(self,pos, r, thickness, colour, transparent_colour, transparency):
        """
        Create blit with star
        create_star_blit(pos,100,5,[255,0,0],[0,0,0],1.0)
        """
        return None


    def plot_centre_blit(self,part, pos):
        """
        Plot an area after rotating preserving centre of the image
        """
        return None


    def plot_rotated_blit(self,part, pos, angle, ellipse_mask=False, transparency=1.0):
        """
        Plot an area after rotating
        """
        return None


    def plot_rotated_centre_blit(self,part, pos, angle, ellipse_mask=False, transpareny=1.0):
        """
        Plot an area after rotating preserving centre of the image
        """
        return None


    def plot_lines(self,line_points, colour, transparency, line_width, avg_height, screen=None, stipple=False, polygons=False):
        """
        Plot a line
        """
        glColor4f(255.0,255.0, 255.0, 0.7)
        glPointSize(5.0)
        glLineWidth(line_width)

        glPushMatrix()
        #glTranslate((400), (400) / 25, (400) / 256)
        #print(line_points)
        lasty=0
        lastx=0
        lastz=0
        for i in range (0,int(len(line_points)/2)):
            x = line_points[i * 2]
            y = line_points[i * 2 + 1]
            #print(x,y)
            if(lastx!=0 and lasty!=0):
                glBegin(GL_LINES)  # GL_POINTS -> GL_LINES
                glVertex3f((lastx * 2 ) / 256, (lastz * 2 - 400) / 256, (lasty * 2 - 400) / 256)
                glVertex3f((x * 2) / 256, (avg_height * 2 - 400) / 256, (y * 2 - 400) / 256)
                glEnd()
            lastx = x
            lasty = y
            lastz=avg_height
        glFlush()
        glPopMatrix()

    def plot_lines_3D(self, line_points, colour, transparency, line_width=1.0, screen=None, stipple=False, polygons=False,edge_sequence=[], plot_mode=0):
        """
        Plot a line
        """
        #print("line_points:",line_points)
        if (plot_mode == 0):
            edge_sequence = vertices_to_edge_sequence(line_points)
        if (plot_mode == 1):
            edge_sequence = basic_vertices_to_edge_sequence(line_points)

        #glPointSize(5.0)
        glPushMatrix()

        glLineWidth(line_width)

        if(stipple==True):
            glLineStipple(1, 0x3F07);
            glEnable(GL_LINE_STIPPLE);

        lasty=0
        lastx=0
        lastz=0
        polygon_detected=False

        if(polygons==True):
            if(edge_sequence is not None and len(edge_sequence)>0):
                glColor4f(255.0, 255.0, 255.0, 0.8)
                polygon_detected = True
            else:
                glColor4f(255.0, 255.0, 255.0, 0.3)

            #glEnable(GL_POLYGON_SMOOTH)
            #glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glBegin(GL_POLYGON)
            #glBegin(GL_TRIANGLES)
        else:
            glColor4f(255.0, 255.0, 255.0, 0.7)
            glBegin(GL_LINES)  # GL_POINTS -> GL_LINES

        col=0.9
        col_index=0
        transparent_factor=0.05
        colour_factor=10

        if (edge_sequence is None or len(edge_sequence)==0):
            #print("Len edge:", len(edge_sequence))
            for i in range (0,int(len(line_points)/3)):
                col-=transparent_factor
                col_index+=colour_factor
                if (polygon_detected == True):
                    glColor4f(255.0, 255.0, 255.0 - col_index, col)
                x = line_points[i * 3]
                y = line_points[i * 3 + 1]
                z = line_points[i * 3 + 2]
                if(i>0):
                    #print(x,y,z)
                    #glBegin(GL_LINES)  # GL_POINTS -> GL_LINES
                    glVertex3f((lastx * 2 ) / 256, (lastz * 2 - 400) / 256, (lasty * 2 - 400) / 256)
                    glVertex3f((x * 2) / 256, (z * 2 - 400) / 256, (y * 2 - 400) / 256)
                    #glEnd()
                lastx = x
                lasty = y
                lastz = z
        else:
            vertices=int(len(line_points)/3)
            #print("Edge sequence",edge_sequence)
            for edge in edge_sequence:
                col-=transparent_factor
                col_index+=colour_factor
                if(polygon_detected==True):
                    glColor4f(255.0, 255.0, 255.0-col_index, col)
                #print("Edge:",edge, " points:",line_points, " vertices:", vertices)
                i_edge = (np.rint(edge)).astype(int)
                if(i_edge.ndim>1):
                    #print("i_edge",i_edge)
                    for int_edge in i_edge:
                        if(int_edge[0] >= vertices):
                            int_edge[0]-= vertices
                        if (int_edge[1] >= vertices):
                            int_edge[1] -= vertices
                        #print(len(line_points),vertices)
                        if(vertices>3):
                            x1 = line_points[int_edge[0] * 3]
                            y1 = line_points[int_edge[0] * 3 + 1]
                            z1 = line_points[int_edge[0] * 3 + 2]
                            x2 = line_points[int_edge[1] * 3]
                            y2 = line_points[int_edge[1] * 3 + 1]
                            z2 = line_points[int_edge[1] * 3 + 2]
                            #glBegin(GL_LINES)  # GL_POINTS -> GL_LINES
                            glVertex3f((x1 * 2) / 256, (z1 * 2 - 400) / 256, (y1 * 2 - 400) / 256)
                            glVertex3f((x2 * 2) / 256, (z2 * 2 - 400) / 256, (y2 * 2 - 400) / 256)
                else:
                    int_edge=i_edge
                    if (int_edge[0] >= vertices):
                        int_edge[0] -= vertices
                    if (int_edge[1] >= vertices):
                        int_edge[1] -= vertices
                    if (vertices > 3):
                        x1 = line_points[int_edge[0] * 3]
                        y1 = line_points[int_edge[0] * 3 + 1]
                        z1 = line_points[int_edge[0] * 3 + 2]
                        x2 = line_points[int_edge[1] * 3]
                        y2 = line_points[int_edge[1] * 3 + 1]
                        z2 = line_points[int_edge[1] * 3 + 2]
                        # glBegin(GL_LINES)  # GL_POINTS -> GL_LINES
                        glVertex3f((x1 * 2) / 256, (z1 * 2 - 400) / 256, (y1 * 2 - 400) / 256)
                        glVertex3f((x2 * 2) / 256, (z2 * 2 - 400) / 256, (y2 * 2 - 400) / 256)
                #glEnd()
        glEnd()
        #glFlush()
        glPopMatrix()

    def drawText(self, x, y, text, pts):
        """
        Draw text at a position on the screen
        """
        font = pygame.font.SysFont('arial', pts)
        textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def help_display_text(self,help_scaling):
        """
        Prototype method to display the scaled help text
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        help_x = 50 + help_scaling
        help_y = 670 - (help_scaling * 10)
        fs = int(22 * (80 - help_scaling) / 80)
        vert_space = 26 * (100 - help_scaling) / 100

        if(self.credits_request==True):
            help_list = help_menu_text.credits_text()
        else:
            help_list = help_menu_text.help_text()
        offset=0
        for line in help_list:
            if(len(line)>0):
                if (offset==0):
                    self.drawText(help_x, help_y - offset * vert_space,line, fs + 4)
                else:
                    self.drawText(help_x, help_y - offset * vert_space, line, fs)
            offset+=1


    def run_help(self):
        """
        Prototype method to update the help screen and listen for keyboard events
        :return: Returns when a key is pressed
        """
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keypress = pygame.key.get_pressed()
        # Check all keys to continue after help screen
        pressed = False
        for keys in keypress:
            if (keys == True):
                pressed = True
        if (pressed == True and self.help_scaling==0):
            self.help_state += 1
            pygame.time.wait(100)
        pygame.time.Clock().tick(100)
        pygame.event.pump()  # process event queue
        if(self.help_scaling>0):
            pygame.display.flip()

    def update_help_state(self):
        """
        State machine for help display
        :return:
        """
        while(self.help_state<3):
            if (self.help_state > 1):
                return True
            if (self.help_state == 0):
                self.help_state = 1

            self.help_scaling -= 3
            if (self.help_scaling) < 0:
                self.help_scaling = 0
            self.help_display_text(self.help_scaling)
            self.run_help()


