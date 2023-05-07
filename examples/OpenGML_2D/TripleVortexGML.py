#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 16th December 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Demo of OpenGML allowing incremental additions of singularities
# =============================================================================

import sys
sys.path.append("../../src/OpenGML")  # AddOpenGML path

import GML_App_2D as app2d
from GML import *
from GML_3D import *
from colour_functions import * #RGB definitions of Colours
from gl_text_drawing import *
import random


def populate_demo(demo_num=0):
    """
    Function to create a simple OpenGML tree
    """
    diameter=8 #Size of the singularity drawn
    freq=30 #Determines the size of the circle that the singularities rotate

    colours=[RED,MAGENTA,YELLOW,CYAN,GREEN,BLUE,PART_RED,PART_YELLOW,PART_CYAN]

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu()

    singluarity=rootNode.add_singularity(180, diameter*0.1, freq * 6.5, WHITE)
    singluarity[0].oscillator_speed_node = 0.00001

    spiral=singluarity[0].add_spiral(0,diameter*0.1, freq * 1.5, RED,3,1,0)

    three_points= rootNode.add_triangle(0, diameter*0.1, freq * 6.5, WHITE)
    three_points[0].oscillator_speed_node = 0.00001
    three_points[1].oscillator_speed_node = 0.00001
    three_points[2].oscillator_speed_node = 0.00001

    #Add seven sided shape
    s1 = three_points[0].add_heptagon(0, diameter * 2, freq * 2.25, WHITE)
    s2 = three_points[1].add_heptagon(0, diameter * 2, freq * 2.25, GREY1)
    s3 = three_points[2].add_heptagon(0, diameter * 2, freq * 2.25, GREY1)
    s4 = spiral.add_heptagon(0, diameter * 1, freq * 2.25, GREY1)
    for s in s2:
        s.oscillator_speed_node = 0.03
    for s in s3:
        s.oscillator_speed_node = -0.03
    for s in s4:
        s.oscillator_speed_node = -0.05

    i=0
    heps=[]
    for s in s1:
        nodes=s.add_singularity(random.randint(-360,360), diameter * 1, freq * 1.5, colours[i])
        #Entangle child nodes
        s2[i].add_child(nodes[0])
        s3[i].add_child(nodes[0])
        s4[i].add_child(nodes[0])
        for node in nodes:
            node.oscillator_speed_node=(random.randint(0,1)*2-1)
            heps.append(node)
        i+=1

    rootNode.set_oscillator_speed(0.81)

    rootNode.oscillator_speed_node=0.01
    for s in s1:
        s.oscillator_speed_node=0.00001

    #Print a text version of the tree
    rootNode.print_tree()
    #Print the GML geometry as text
    print("GML geometry text representation: ", rootNode.gml_to_text(100))

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML 2D Arithmetic", populate_demo)
    app.initial_rotation_speed(1)
    app.balancing_phases(False)
    app.mode_2d=3
    app.set_depth_projection(False)
    app.run2d()