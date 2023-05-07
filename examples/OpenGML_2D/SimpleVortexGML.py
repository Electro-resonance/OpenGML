#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 17th December 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Demo of OpenGML showing entanglement between different areas
# implemented by sharing nodes between distinct singularities.
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

    two_points= rootNode.add_dipole(0, diameter*0.1, freq * 6.5, WHITE)
    two_points[0].oscillator_speed_node = 0.00001
    two_points[1].oscillator_speed_node = 0.00001

    #Add seven sided shape
    s1= two_points[0].add_heptagon(0, diameter*3, freq * 2.25, WHITE)
    s2= two_points[1].add_heptagon(0, diameter * 3, freq * 2.25, GREY1)
    for s in s2:
        s.oscillator_speed_node = 0.03

    i=0
    heps=[]
    for s in s1:
        nodes=s.add_singularity(random.randint(-360,360), diameter * 2, freq * 1.5, colours[i])
        #Entangle child nodes
        s2[i].add_child(nodes[0])
        for node in nodes:
            node.oscillator_speed_node=(random.randint(0,1)*2-1)
            heps.append(node)
        i+=1

    rootNode.set_oscillator_speed(1.71)

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
    app = app2d.GML_App_2D("Spiralling Triangles", populate_demo)
    app.initial_rotation_speed(1)
    app.balancing_phases(False)
    app.mode_2d=3
    app.set_depth_projection(False)
    app.run2d()