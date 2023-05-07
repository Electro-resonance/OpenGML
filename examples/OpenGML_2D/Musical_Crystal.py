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
import random


def populate_demo(demo_num=0):
    """
    For a given demo number construct the GML tree for that demo
    """

    # Define the shapes to use at each level of the yantra
    shapes = ["triangle", "square", "pentagon", "hexagon"]

    # Set up the size and frequency parameters
    diameter = 20  # Diameter of the central circle
    freq = 35  # Frequency of the yantra

    # Define the colors to use for the shapes
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

    # Create a tiny point as the starting root node for the GML tree
    rootNode = create_bindu()

    # Recursive function to add shapes at each level of the yantra
    def add_shapes(node, level, freq_offset=0, freq_incr=0.2):
        if level == 0:
            return
        else:
            # Choose a random shape and color for this level
            shape = random.choice(shapes)
            color = random.choice(colors)

            # Add the shape to the current node
            node2=node.add_shape(shape, diameter * level * 0.1, freq * level + freq_offset, color)

            freq_offset+=freq_incr
            freq_incr+=0.1

            # Recursively add shapes to each child node
            for child in node2:
                add_shapes(child, level - 1, freq_offset, freq_incr)

    # Call the recursive function to build the yantra
    node = rootNode.add_singularity(0, diameter * 0.1, 0.5 * freq, colors[0])
    add_shapes(node[0], 4)

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML 2D Arithmetic", populate_demo, sonic_enabled=True)
    app.initial_rotation_speed(0.2)
    app.balancing_phases(False)
    app.set_depth_projection(False)
    app.run2d()