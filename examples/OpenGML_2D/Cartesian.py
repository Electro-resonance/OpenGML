#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 18th June 2022
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

def populate_demo(demo_num=0):
    """
    Function to create a simple OpenGML tree
    """
    diameter=8 #Size of the singularity drawn
    freq=30 #Determines the size of the circle that the singularities rotate

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu()

    size=20

    #Add tangential points to the root node
    s1=rootNode.add_singularity(0, diameter * 3, freq * size, RED)
    s2=rootNode.add_singularity(90, diameter * 3, freq * size, RED)

    #Emphasise Bindu
    rootNode.add_singularity(-270, diameter * 2, freq * 0.001, YELLOW)

    for a in range(1,29):
        b=a/(size/4)+(size-3)
        s3=s1[0].add_singularity(0, diameter * 1, freq * b, GREEN)
        s4=s2[0].add_singularity(90, diameter * 1, freq * b, CYAN)

    rootNode.set_oscillator_speed(1.71)

    #Print a text version of the tree
    rootNode.print_tree()
    #Print the GML geometry as text
    print("GML geometry text representation: ", rootNode.gml_to_text(200))

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML 2D Cartesian", populate_demo)
    app.initial_rotation_speed(0)
    app.run2d()

