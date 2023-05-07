#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 3rd June 2022
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
    freq=15 #Determines the size of the circle that the singularities rotate

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu()

    #Add a single point to the root node
    rootNode.add_singularity(0, diameter*3, freq*17, RED)

    #Add a dipole to the root node
    s1=rootNode.add_dipole(0, diameter*1.1, freq*1.5, MAGENTA)

    #Add a triangle to first point of the dipole.
    s2=s1[0].add_triangle(0, diameter*1.2, freq*6.7, YELLOW)

    #Add a square to second corner of the triangle
    s3=s2[1].add_square(0,   diameter*1.3, freq*2.3, CYAN)

    #Add a pentagon to fourth corner of the square.
    s4=s3[3].add_pentagon(0, diameter*1.4, freq*8, GREEN)

    #Add small triangles at three of the corners of the pentagon
    s4[0].add_triangle(0, diameter, freq*1.4, WHITE)
    s4[2].add_triangle(0, diameter, freq*0.7, WHITE)
    s4[4].add_triangle(0, diameter, freq*0.7, WHITE)

    #Print a text version of the tree
    rootNode.print_tree()
    #Print the GML geometry as text
    print("GML geometry text representation: ", rootNode.gml_to_text(100))

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("Simple GML", populate_demo)
    app.initial_rotation_speed(0.3)
    app.balancing_phases(False)
    app.mode_2d=3
    app.set_depth_projection(False)
    app.run2d()
