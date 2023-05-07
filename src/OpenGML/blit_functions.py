# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 22nd March 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Helper functions for 2D blit objects with Kivy
# =============================================================================

import math
import trig_tables as trig
from kivy.graphics import *
from kivy.graphics import Line, Color
from kivy.graphics.texture import Texture
from kivy.graphics import Mesh
from kivy.graphics.tesselator import Tesselator
from kivy.graphics import gl_instructions
from kivy.clock import Clock

import numpy as np

import gl_text_drawing as gl
from graphics_helper import GraphicsHelperBaseClass
import menu_functions as help_menu_text

class BlitGraphicsHelper(GraphicsHelperBaseClass):

    def init(self,window1):
        """
        Set up the global variable pointing to the Pygame screen
        """
        self.window = window1
        self.screen_width, self.screen_height = self.window.size
        #self.screen_width, self.screen_height = self.screen_get_screen_size()

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


    def get_pixel_colors(self,texture, dims):
        """
        Return an array of [rgba] for colours of the given texture
        """
        return None

        pos = (0, 0)
        #print("Image size",dims)
        pixel = texture.get_region(pos[0], pos[1], dims[0], dims[1])
        bp = pixel.pixels
        data = np.frombuffer(bp, dtype=np.uint8).reshape(dims[0], dims[1]*4)
        #print("TextureRegion.pixels = \n", data)
        return data


    def get_pixel_color(self,colour_array, image_dims, pos):
        """
        Return the colour at a point in an array representing a photo
        """
        h = image_dims[1]
        w = image_dims[0]
        index1 = int((pos[0]))
        index2 = int((pos[1])*4)
        #print("Shape=",colour_array.shape)
        #print("Position=",pos)
        #print("Index=",index1,index2)
        if(index1 < 0 or index2 < 0 or index1 > colour_array.shape[0] or index2 > colour_array.shape[1]):
            print("Point outside of image")
            return BACKGROUND

        col = (colour_array[index1, index2+0], colour_array[index1, index2+1],
               colour_array[index1, index2+2], colour_array[index1, index2+3])
        #print("Col=",col)
        return col


    def grab_circular_photo_blit(self,im, colour_array, image_dims, image_scale, texture, x, y, w, h, transparent_colour, scale):
        """
        Grab an area from a photo
        """
        #print(colour_array.shape,image_dims)
        if(w < 10):
            w = 10
        if(h < 10):
            h = 10

        u1 = 2
        v1 = 2
        w1 = 2
        h1 = 2
        loop_count = 0
        while True:
            loop_count += 1
            u1 = (x-w*6)/(image_dims[0]/image_scale)
            v1 = (y-h*6)/(image_dims[1]/image_scale)
            w1 = w/(image_dims[0]/image_scale)*12
            h1 = h/(image_dims[1]/image_scale)*12
            if((u1+w1) < 1 and (v1+h1) < 1 and u1 > 0 and v1 > 0):
                break
            if(loop_count > 10):
                if(loop_count > 20):
                    break
                w = w*0.5
                h = h*0.5
            else:
                w = w*0.95
                h = h*0.95

        #print("!!!!    ",int(x),int(y),u1,v1,w1,h1)
        texc = u1, v1, u1 + w1, v1, u1 + w1, v1 + h1, u1, v1 + h1

        w = w*6
        h = h*6

        with self.canvas:
            self.fbo = Fbo(size=(w/w1, h/h1))
            self.fbo.bind()
            self.fbo.clear_buffer()
            self.fbo.release()
            with self.fbo:
                Color(1, 1, 1, 1)
                Rectangle(pos=(0, 0), size=(
                    image_dims[0]/6, image_dims[1]/6), texture=texture, tex_coords=texc)

        #single_colour=get_pixel_color(colour_array,image_dims,[x*image_scale,y*image_scale]) #-w, y-h])
        if(x < 0):
            x = 0
        if(y < 0):
            y = 0
        try:
            s_colour = im.read_pixel(x*image_scale, image_dims[1]-(y*image_scale))
        except:
            s_colour = [0, 0, 0]
        single_colour = [s_colour[0]*255, s_colour[1]*255, s_colour[2]*255, 255]
        #colour=[255,255,255,127]
        return [w, h, self.fbo, single_colour]


    def create_spiral_blit(self,pos, r, line_width, colour, transparent_colour, transparency, gears, phase, spiral_rate, spiral_mode, extra_angle):
        """
        Create blit with spiral
        """
        if(r < 1):
            r = 1
        size = (r*2, r*2)
        with self.canvas:
            colour = [colour[0]/256, colour[1]/256, colour[2]/256, 0.9]
            Color(colour)
            if(line_width == 0):
                r_width = r/2
                Line(circle=(pos[0], pos[1], r_width), width=r_width)
            else:
                Line(circle=(pos[0], pos[1], r), width=1.5)

        oversize = 1.4
        r_over = r*oversize
        with self.canvas:
            self.fbo = Fbo(size=(2*r_over, 2*r_over))
            Rectangle(pos=(pos[0]-r_over, pos[1]-r_over),
                      size=(2*r_over, 2*r_over), texture=self.fbo.texture)
        with self.fbo:
            ClearColor(0, 0, 0, 0.5)
            if(line_width == 0):
                r_width = r/2
                Color(colour[0], colour[1], colour[2], 1.0)
                Line(circle=(r_over, r_over, r_width), width=r_width)
                Color(0, 0, 0, 0)

            else:
                Color(colour[0], colour[1], colour[2], 1.0)
                #Line(circle=(r_over, r_over, r),width=2.0)
                for j in range(0, 722):
                    k = j/2
                    ph = k*spiral_rate
                    if(spiral_mode == 1):
                        r1 = abs(k/180-1)*r
                    elif(spiral_mode == 2):
                        r1 = (k/180-1)*r
                        if(k >= 180):
                            ph = -ph
                    elif(spiral_mode == 3):
                        if(k >= 180):
                            k2 = (360-k)*2
                        else:
                            k2 = k*2
                        r1 = (k2/180-1)*r
                        if(k2 >= 180):
                            ph = -ph
                    else:
                        r1 = k/360*r
                    if(extra_angle != 0):
                        if(r1 > 0):
                            ph = ph+extra_angle
                    x1 = r1*trig.fast_cos(ph/180*math.pi) + r_over
                    y1 = r1*trig.fast_sin(ph/180*math.pi) + r_over
                    if(k == 0):
                        x2 = x1
                        y2 = y1
                    Line(points=[x1, y1, x2, y2], width=2.0)
                    x2 = x1
                    y2 = y1
                Color(0, 0, 0, 0)
        self.fbo.draw()
        return [r_over, r_over, self.fbo]


    def create_circular_blit(self,pos, r, line_width, colour, transparent_colour, transparency, gears, phase):
        """
        Create blit with circle
        """
        #gears=True
        #line_width=2
        #r=120
        if(r < 1):
            r = 1
        if(gears == True):
            r = r*1.3
        size = (r*2, r*2)
        with self.canvas:
            colour = [colour[0]/256, colour[1]/256, colour[2]/256, 0.9]
            Color(colour)
            if(line_width == 0):
                r_width = r/2
                Line(circle=(pos[0], pos[1], r_width), width=r_width)
            else:
                Line(circle=(pos[0], pos[1], r), width=1.5)
                #Line(circle=(pos[0], pos[1], r+1),width=1.0)

        if(gears == False):
            oversize = 1.4
        else:
            oversize = 1.0
        r_over = r*oversize
        with self.canvas:
            self.fbo = Fbo(size=(2*r_over, 2*r_over))
            #Color(1, 1, 0.8)
            Rectangle(pos=(pos[0]-r_over, pos[1]-r_over),
                      size=(2*r_over, 2*r_over), texture=self.fbo.texture)
        with self.fbo:
            ClearColor(0, 0, 0, 0.5)
            #Color(0, 0, 0, 0.8)
            #Rectangle(size=(r, r))
            #ClearBuffers()
        #fbo.bind()
        #fbo.clear_buffer()
            #Color(colour[0]/256,colour[1]/256,colour[2]/256,0.5)
            #Rectangle(pos=(0,0), size=(2*r,2*r))
            #Color(colour[0]/256,colour[1]/256,colour[2]/256,0.9)
            #Color(1,colour[1]/256,colour[2]/256,0.9)
            if(line_width == 0):
                r_width = r/2
                if(gears == False):
                    Color(colour[0], colour[1], colour[2], 1.0)
                    Line(circle=(r_over, r_over, r_width), width=r_width)
                    Color(0, 0, 0, 0)
                else:
                    Color(colour[0], colour[1], colour[2], 1.0)
                    Line(circle=(r, r, r), width=line_width)
                    spokes = int((r/20)+3)
                    for k in range(spokes+3):
                        x1 = 0.48*r*trig.fast_cos(2*math.pi*k/spokes) + r
                        y1 = 0.48*r*trig.fast_sin(2*math.pi*k/spokes) + r

                        if (k > 0):
                            if(spokes > 6):
                                x2 = 0.98*r*trig.fast_cos(2*math.pi*k/spokes) + r
                                y2 = 0.98*r*trig.fast_sin(2*math.pi*k/spokes) + r
                                #Color(colour[0],colour[1],colour[2],1.0)
                                Line(points=[r, r, x2, y2], width=10)
                                #Color(colour[0],colour[1],colour[2],1.0)
                                Line(circle=(x1, y1, int(r/2)), width=4)
                    Color(0, 0, 0, 0)

                #for r1 in range(int(r+20),int(2*r)):
                #    Line(circle=(r_over, r_over, r1),width=1)
            else:
                Color(colour[0], colour[1], colour[2], 1.0)
                Line(circle=(r_over, r_over, r), width=2.0)
                Color(0, 0, 0, 0)
                #for r1 in range(int(r+30),int(2*r)):
                #    Line(circle=(r_over, r_over, r1),width=1)
                #Color(0,0,0,0)
                #for r1 in range(int(r+2),int(2*r)):
                #    Line(circle=(r, r, r1),width=1)

            #Line(circle=(r, r, r),width=1.5)

        #fbo.release()
        self.fbo.draw()
        if(gears == True):
            self.plot_rotated_centre_blit([r, r, self.fbo], (pos[0], pos[1]), phase)

            #canvas_img = Canvas() #Image.new('RGB', (int(2*r), int(2*r)), color=(255,255,255,255))

        # circle_surface = pygame.Surface(size, pygame.SRCALPHA)
        # circle_surface.set_colorkey(transparent_colour)  # Transparent black
        # circle_surface.set_alpha(transparency)  # Transparency 50% = 127
        # if(gears==True):
        #     pygame.draw.circle(circle_surface, colour, (r, r), r, line_width)
        #     spokes=int((r/20)+3)
        #     for k in range(spokes+3):
        #         x1 = 0.48*r*trig.fast_cos(2*math.pi*k/spokes) + r
        #         y1 = 0.48*r*trig.fast_sin(2*math.pi*k/spokes) + r
        #
        #         if (k>0):
        #             if(spokes>6):
        #                 x2 = 0.98*r*trig.fast_cos(2*math.pi*k/spokes) + r
        #                 y2 = 0.98*r*trig.fast_sin(2*math.pi*k/spokes) + r
        #                 pygame.draw.line(circle_surface, colour, [x2, y2], [r, r], 10)
        #
        #             pygame.draw.circle(circle_surface, colour, (x1, y1), int(r/2), 4)
        #
        #     circle_surface=plot_rotated_centre_blit(circle_surface, (pos[0],pos[1]),phase)
        # else:
        #     pygame.draw.circle(circle_surface, colour, (r, r), r, line_width)
        #
        #     screen.blit(circle_surface, (pos[0]-r,pos[1]-r))
        #return circle_surface
        return [r_over, r_over, self.fbo]


    def grab_circular_colour(self,image1, r):
        """
        Grab colour from the middle of an area
        """
        if(image1 == None):
            print("grab_circular empty")
            return [80, 80, 80]
        if(r < 1):
            r = 1
        #x, y = image1.texture_size()
        #print(int(r/4),x,y)
        #if(x==0 or y==0):
        #    return [200,200,200]
        #else:
        #colour=image1.texture.get_pixel_color(int(r/4),int(r/4))
        with self.canvas:
            colour = self.et_pixel_color(image1.texture, [int(r/4), int(r/4)])
        #print("test1",colour)
            #im = Window.screenshot()
            #image1 = Image.load(im, keep_data=True)
            #colour = image1.read_pixel(int(r/4),int(r/4))
        return colour[0] * 255, colour[1] * 255, colour[2] * 255


    def create_star_blit(self,pos, r, thickness, colour, transparent_colour, transparency):
        """
        Create blit with star
        create_star_blit(pos,100,5,[255,0,0],[0,0,0],1.0)
        """
        oversize = 1.4
        r_over = r*oversize
        with self.canvas:
            self.fbo = Fbo(size=(2*r_over, 2*r_over))
            Rectangle(pos=(pos[0]-r_over, pos[1]-r_over),
                      size=(2*r_over, 2*r_over), texture=self.fbo.texture)
        with self.fbo:
            ClearColor(0, 0, 0, 0.5)
            Color(colour[0], colour[1], colour[2], transparency)
            if(r < 1):
                r = 1
            size = (r*2, r*2)
            #star_surface = pygame.Surface(size, pygame.SRCALPHA)
            #star_surface.set_colorkey(transparent_colour)  # Transparent black
            #star_surface.set_alpha(transparency)  # Transparency 50% = 127
            for k in range(6):
                x1 = r*trig.fast_cos(4*math.pi*k/5 + 0.5*math.pi) + r
                y1 = r*trig.fast_sin(4*math.pi*k/5 + 0.5*math.pi) + r
                if(k > 0):
                    Line(points=[x1, y1, x2, y2], width=thickness)
                x2 = x1
                y2 = y1
            #screen.blit(star_surface, (pos[0]-r,pos[1]-r))
        self.fbo.draw()
        return [r, r, self.fbo]


    def plot_centre_blit(self,part, pos):
        """
        Plot an area after rotating preserving centre of the image
        """
        with self.canvas:
            r1 = part[0]
            r2 = part[1]
            Rectangle(pos=(pos[0]-r1, pos[1]-r2),
                      size=(2*r1, 2*r2), texture=part[2].texture)
        return [r1, r2, part]


    def plot_rotated_blit(self,part, pos, angle, ellipse_mask=False, transparency=1.0):
        """
        Plot an area after rotating
        """
        with self.canvas:
            r1 = part[0]
            r2 = part[1]
            PushMatrix()
            Rotate(angle=angle, origin=(pos[0], pos[1]))

            if(ellipse_mask == True):
                StencilPush()
                Ellipse(pos=(pos[0], pos[1]), size=(2*r1, 2*r2))
                StencilUse()
            Color(1, 1, 1, transparency)
            Rectangle(pos=(pos[0], pos[1]), size=(
                2*r1, 2*r2), texture=part[2].texture)
            if(ellipse_mask == True):
                StencilPop()
            PopMatrix()
        return [r1, r2, part]


    def plot_rotated_centre_blit(self,part, pos, angle, ellipse_mask=False, transpareny=1.0):
        """
        Plot an area after rotating preserving centre of the image
        """
        with self.canvas:
            r1 = part[0]
            r2 = part[1]
            PushMatrix()
            Rotate(angle=angle, origin=(pos[0], pos[1]))

            if(ellipse_mask == True):
                StencilPush()
                Ellipse(pos=(pos[0]-r1, pos[1]-r2), size=(2*r1, 2*r2))
                StencilUse()
            Color(1, 1, 1, transpareny)
            Rectangle(pos=(pos[0]-r1, pos[1]-r2),
                      size=(2*r1, 2*r2), texture=part[2].texture)
            if(ellipse_mask == True):
                StencilPop()
            PopMatrix()
        return [r1, r2, part]


    def plot_lines(self,line_points, colour, transparency=0.5, line_width=1.0,  avg_height=1.0, screen=None, stipple=False,polygons=False):
        """
        Plot a line
        """
        if(screen is not None):
            self.canvas=screen
        if(self.canvas is None):
            print("plot lines failed as no screen")
            #return
        with self.canvas:
            PushMatrix()
            #r1=part[0]
            #r2=part[1]
            #PushMatrix()
            ClearColor(0, 0, 0, 0.5)
            if(polygons==True and len(line_points)>6):
                Color(colour[0], colour[1], colour[2], transparency)
                tess = Tesselator()
                tess.add_contour(line_points)
                if not tess.tesselate():
                    print("Tesselator didn't work")
                else:
                    # Add the meshes to the canvas
                    for vertices, indices in tess.meshes:
                        self.canvas.add(Mesh(
                            vertices=vertices,
                            indices=indices,
                            mode="triangle_fan"
                        ))
                Color(colour[0], colour[1], colour[2], 1.0)
            else:
                Color(colour[0], colour[1], colour[2], 1.0)
                Line(points=line_points, width=line_width)
            PopMatrix()
        #return [r1,r2,part]



    def help_display_text(self, help_scaling):
        """
        Prototype method to display the scaled help text
        """
        def help_display_callback(dt):
            """
            Sub function for timed callback
            """
            help_x = 50 + help_scaling
            help_y = 540 - (help_scaling * 10)
            fs = int(22 * (80 - help_scaling) / 80)
            vert_space = 26 * (100 - help_scaling) / 100

            if (self.credits_request==True):
                help_list = help_menu_text.credits_text()
            else:
                help_list = help_menu_text.help_text()
            offset=0
            self.canvas.clear()
            ft=gl.FreeDrawText()
            for line in help_list:
                if(len(line)>0):
                    if (offset==0):
                        ft.drawText(self.canvas, help_x, help_y - offset * vert_space,line, fs + 4,colour=[1,1,0,1])
                    else:
                        ft.drawText(self.canvas, help_x, help_y - offset * vert_space,line, fs,colour=[1,1,0,1])
                offset+=1

        event = Clock.schedule_once(help_display_callback,0.05)
        event()


    def run_help(self):
        """
        Prototype method to update the help screen and listen for keyboard events
        :return: Returns when a key is pressed
        """
        return

    def update_help_state(self):
        """
        State machine for help display
        :return:
        """
        if (self.help_state == 0):
            self.help_state = 1
        if (self.help_state >= 2):
            return True
        self.help_scaling -= 3
        if (self.help_scaling) < 0:
            self.help_scaling = 0
        if (self.help_scaling) >= 0:
            self.help_display_text(self.help_scaling)
        return False

    def key_pressed(self, keycode):
        """
        Accept key presses from engine
        :return:
        """
        if(self.help_state == 1):
            self.help_state=2
        elif (keycode=='h'):
            self.credits_request = False
            self.help_state = 0
            self.help_scaling = 100
        elif (keycode=='y'):
            self.credits_request = True
            self.help_state = 0
            self.help_scaling = 100
