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

    # Set up the size and frequency parameters
    diameter = 12  # Diameter of the central circle
    freq = 5  # Frequency of the yantra

    # Define the colors to use for the shapes
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

    # Define the shapes to use at each level
    shapes = [
        ["circle", "triangle", "square", "pentagon"],
        ["triangle", "square", "circle", "pentagon"],
        ["square", "circle", "triangle", "pentagon"],
        ["pentagon", "circle", "square", "triangle"],
    ]

    # Create a tiny point as the starting root node for the GML tree
    rootNode = create_bindu()

    # Recursive function to add shapes to a node
    def add_shapes(node, level):
        if level == 0:
            return
        else:
            for i in range(len(shapes[level])):
                shape = shapes[level][i]
                color = colors[i % len(colors)]
                distance = (level + 1) * diameter * 2
                size = freq * distance / 100
                new_node = node.add_shape(shape, diameter * level * 0.1, freq * (level + 1 +i)*size, color)
                # Recursively add shapes to each child node
                for child in new_node:
                    add_shapes(child, level - 1)

    node = rootNode.add_singularity(0, diameter * 1, freq*40, colors[0])
    # Add shapes with different sizes of the first circle
    add_shapes(node[0], 2)

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML 2D Flower of Music", populate_demo, sonic_enabled=True)
    app.initial_rotation_speed(0.5)
    app.balancing_phases(False)
    app.set_depth_projection(False)
    app.run2d()