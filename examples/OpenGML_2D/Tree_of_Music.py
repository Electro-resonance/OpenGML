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
    Populate the demo with a nested tree using an array of shape descriptions to
    define the shapes used at each level.
    """

    # Set up the size and frequency parameters
    diameter = 12  # Diameter of the central circle
    freq = 6 # Frequency of the yantra

    # Define the colors to use for the shapes
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

    # Define the shapes to use at each level
    shapes = [
        ["pentagon", "pentagon"],
        ["triangle", "pentagon"],
        ["pentagon", "triangle"],
        ["pentagon", "triangle"],
        ["triangle", "square"],
        ["pentagon", "pentagon"],
        ["pentagon", "triangle"],
        ["triangle", "square"],
        ["square", "triangle"]
    ]

    # Create a tiny point as the starting root node for the GML tree
    rootNode = create_bindu()

    # Recursive function to add shapes to a node
    def add_shapes(node, level):
        if level == 0:
            return
        else:
            for i in range(len(shapes[level])):
                shape = shapes[level+i][i]
                color = colors[(i+level) % len(colors)]
                distance = (level +i  + 1) * diameter * 2
                size = freq * distance / 100
                new_node = node.add_shape(shape, diameter * level * 0.1, freq * (level + 1 + i) * size, color)
                # Recursively add shapes to each child node
                for child in new_node:
                    add_shapes(child, level - 1)

    # Add the central circle
    node = rootNode.add_singularity(0, diameter * 1, freq * 70, colors[0])

    add_shapes(node[0], 2)

    rootNode.set_oscillator_speed(0.5)
    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML 2D Arithmetic", populate_demo, sonic_enabled=True)
    app.initial_rotation_speed(1)
    app.balancing_phases(False)
    app.set_depth_projection(False)
    app.run2d()