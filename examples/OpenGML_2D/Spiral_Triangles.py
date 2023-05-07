#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 28th April 2023
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
    For a given demo number construct the GML tree for that demo
    """

    # Set up the size and frequency parameters
    diameter = 10  # Diameter of the central circle
    freq = 7  # Frequency of the yantra

    # Define the colors to use for the triangles
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

    # Create a tiny point as the starting root node for the GML tree
    rootNode = create_bindu()

    # Add a single point to the root node
    currNode=rootNode.add_singularity(0, diameter * 3, freq * 1, RED)

    # Add the nested triangles
    for i in range(1, 40):
        color = colors[i % len(colors)]
        currNode = currNode[0].add_triangle(0, diameter * i * 0.1, freq * (i + 1), color)


    rootNode.set_oscillator_speed(1.71)
    rootNode.set_oscillator_speed(0.5)
    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("Spiralling Triangles", populate_demo)
    app.initial_rotation_speed(1)
    app.balancing_phases(False)
    app.mode_2d=3
    app.set_depth_projection(False)
    app.run2d()