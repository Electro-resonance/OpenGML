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
    freq = 10  # Frequency of the yantra

    # Define the colors to use for the squares
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

    # Create a tiny point as the starting root node for the GML tree
    rootNode = create_bindu()

    # Add the arms emanating from the central Bindu
    num_arms = 1  # Number of arms
    arm_angle = 360 / num_arms  # Angle between arms
    for i in range(num_arms):
        #arm_node = rootNode.add_singularity(0, diameter * 3, freq * (i + 1), colors[i % len(colors)])

       # arm_node[0].set_phase(arm_angle * i)

        # Add the nested triangles to each arm
        for j in range(0, 36):
            color = colors[j % len(colors)]
            currNode = rootNode.add_triangle(0, diameter * j * 0.1, freq * (j + 1), color)

    rootNode.set_oscillator_speed(0.5)
    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML 2D Arithmetic", populate_demo, sonic_enabled=True)
    app.initial_rotation_speed(1)
    app.balancing_phases(False)
    app.set_depth_projection(False)
    app.run2d()