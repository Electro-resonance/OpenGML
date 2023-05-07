#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../../src/OpenGML") #AddOpenGML path

import GML_App_3D as app3d
from GML import *
from GML_3D import *
from colour_functions import *
import pygame

demo_num=0

def populate_demo(demo_num):
    diameter=8
    freq=30

    if(demo_num==0):
        #Hello OpenGML Universe
        rootNode=create_bindu()
        rootNode.add_polygon("ReducingPoly", 5, 0, diameter*1.5, freq*10, GREEN2, 3, 0.1,-2,+1,True)
    elif(demo_num==1):
        rootNode=create_bindu()
        rootNode.add_polygon("ReducingPoly", 9, 0, diameter*1.5, freq*10, GREEN2, 3, 0.1,-1,-1,True)
    elif(demo_num==2):
        rootNode=create_bindu()
        rootNode.add_polygon("NestedPoly5", 5, 0, diameter*1.3, freq*8, GREEN2, 3, 0.15,-1)
        rootNode.add_polygon("NestedPoly6", 6, 0, diameter*1.4, freq*4, MAGENTA, 3, 0.3,-1)
        rootNode.add_polygon("NestedPoly4", 4, 0, diameter*1.5, freq*2, YELLOW, 3, 0.4,-1)
    elif(demo_num==3):
        rootNode=create_bindu()
        rootNode.add_pentagon(0, diameter,   freq,   RED)
        rootNode.add_square(0,   diameter,   freq*3, MAGENTA, 2, 0.3) #Nested 2 deep
        rootNode.add_heptagon(0, diameter,   freq*6, YELLOW, 3, 0.2) #Nested 3 deep
        rootNode.add_triangle(0, diameter*2, freq*8, GREEN2, 2, 0.1) #Nested 2 deep
    elif(demo_num==4):
        rootNode=create_bindu()
        rootNode.add_singularity(0, diameter*1, freq*2, RED)
        rootNode.add_dipole(0, diameter*2, freq*4, MAGENTA)
        rootNode.add_triangle(0, diameter*3, freq*6, YELLOW)
        rootNode.add_square(0,   diameter*4,   freq*8, GREEN2)
        rootNode.add_pentagon(0, diameter*5,   freq*10, BLUE_PURPLE)
    elif(demo_num==5):
        rootNode=create_bindu()
        rootNode.add_polygon_list("PolyList",[3,3,1,1,1,0,1,0,1,0,2,4,0,0,0,0,0,5,0,0,0,0,0],0, diameter*1, freq*4, MAGENTA,0.5,True)
    elif(demo_num==6):
        rootNode=create_bindu()
        rootNode.add_polygon_list("PolyList",[1,1,1,1,1,1,1,1,2,1,1,1,1,0,1,1,1,1,0],0, diameter*1, freq*4, YELLOW,0.8,True)
    elif(demo_num==7):
        #Generalised Neuron implementing Figure 6.14 of "NanoBrain The Making of an Artificial Brain from a Time Crystal" by Anirban Bandyopadhyay.
        rootNode=create_bindu()
        rootNode.add_polygon_list("Neuron",
        [3,
        4, 3,1,0,1,0,1,0, 4,1,0,1,0,1,0,1,0, 3,1,0,1,0,1,0, 2,1,0,3,1,0,1,0,1,0,
        4, 2,1,0,1,0, 2,1,0,1,0, 4,1,0,1,0,1,0,1,0, 3,1,0,1,0,1,0,
        4, 1,0, 1,0, 1,0, 3,3,1,0,1,0,1,0, 3,1,0,1,0,1,0, 2,1,0, 3,1,0,1,0, 2,1,0, 3,1,0,1,0,1,0],
        0, diameter*1, freq*7, GREEN2,0.5,True)
    elif(demo_num>=8):
        rootNode=create_bindu()
        rootNode.add_polygon_list("PolyList",[2,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,2,1,1,1,1,0,1,1,1,1,1,1,1,0],0, diameter*1, freq*4, YELLOW,0.8,True)

    return rootNode

app=None

def callback_mode(key):
    global demo_num
    global app
    demo_num += 1
    print("Demo mode:",demo_num)
    if (demo_num > 8):
        demo_num = 0
    if (demo_num == 6 or demo_num == 8):
        app.set_depth_projection(True)
    else:
        app.set_depth_projection(False)

if __name__ == '__main__':
    #Run the app
    app=app3d.GML_App_3D("OpenGML Basic Cube",populate_demo,plan_mode=2)
    app.initial_rotation_speed(0)
    app.add_key_callback(pygame.K_w,callback_mode,True)
    app.set_zoom_relative(-4) #Zoom out
    app.run()