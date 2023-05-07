#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("../../src/OpenGML")  # AddOpenGML path

import GML_App_3D as app3d
from GML import *
from GML_3D import *
from colour_functions import *

def populate_demo(demo_num):
    """
    Function to create a simple OpenGML flower with rotating petals
    Created from a dialog with ChatGPT after providing examples of the
    syntax of OpenGML. ChatGPT3 was asked to create code for a colourful
    demonstration of 3D OpenGML. this is the resulting code.
    """
    diameter = 1 #Size of the singularity drawn
    freq = 3 #Determines the size of the circle that the singularities rotate
    phase_offset = 0.5 #Determines the phase offset of the rotating petals

    # Create a tiny point as starting root node for the GML tree
    rootNode = create_bindu()

    # Add a single point to the root node
    s2=rootNode.add_singularity(0, diameter*3, freq*17, RED)

    # Add a pentagon to the root node
    s1 = s2[0].add_pentagon(0, diameter*1.1, freq*1.5, YELLOW)

    # Add triangles to each corner of the pentagon
    s1[0].add_triangle(0, diameter*1.2, freq*6.7, MAGENTA)
    s1[1].add_triangle(0, diameter*1.2, freq*6.7, BLUE)
    s1[2].add_triangle(0, diameter*1.2, freq*6.7, CYAN)
    s1[3].add_triangle(0, diameter*1.2, freq*6.7, GREEN)
    s1[4].add_triangle(0, diameter*1.2, freq*6.7, ORANGE)

    rootNode.set_oscillator_speed(1.71)

    # Print a text version of the tree
    rootNode.print_tree()
    # Print the GML geometry as text
    print("GML geometry text representation: ", rootNode.gml_to_text(100))

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML 2D Example", populate_demo)
    app.initial_rotation_speed(1)
    app.run()