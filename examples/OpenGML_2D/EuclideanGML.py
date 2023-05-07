#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 27th February 2023
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

    s1 = rootNode.add_euclidean_rhythm("Outer", events=7, steps=13, diameter=diameter * 1, freq=freq * 9, colour=GREEN)
    s2 = rootNode.add_euclidean_rhythm("Inner2", events=9, steps=13,diameter=diameter * 1, freq=freq * -7,colour=MAGENTA)
    s3 = rootNode.add_euclidean_rhythm("Inner1", events=5, steps=7, diameter=diameter * 1, freq=freq * 5,colour=CYAN)
    s4 = rootNode.add_euclidean_rhythm("Inner", events=3, steps=5, diameter=diameter * 1, freq=freq * -3,colour=GREEN)

    s1[0].add_euclidean_rhythm("Dipole", events=2, steps=4, diameter=diameter * 0.5, freq=freq * 1, colour=YELLOW)
    #s1[1].add_euclidean_rhythm("Dipole", events=2, steps=5, diameter=diameter * 1.0, freq=freq * 0.5, colour=grey)
    #ys2 = s1[2].add_euclidean_rhythm("Triangle", events=3, steps=5, diameter=diameter * 0.5, freq=freq * 0.5, colour=grey)
    #ys3 = ys2[2].add_euclidean_rhythm("Triangle", events=3, steps=5, diameter=diameter * 0.5, freq=freq * 1.0,colour=grey)
    #ys4 = ys3[2].add_euclidean_rhythm("Triangle", events=3, steps=5, diameter=diameter * 0.5, freq=freq * 1.5,colour=grey)
    #s1[3].add_euclidean_rhythm("Dipole", events=4, steps=5, diameter=diameter * 1.0, freq=freq * 0.5, colour=grey)
    #s1[4].add_euclidean_rhythm("Dipole", events=5, steps=7, diameter=diameter * 1.0, freq=freq * 0.3, colour=grey)
    #s1[5].add_euclidean_rhythm("Dipole", events=6, steps=7, diameter=diameter * 1.0, freq=freq * 0.5, colour=grey)
    #s1[6].add_euclidean_rhythm("Dipole", events=7, steps=9, diameter=diameter * 1.0, freq=freq * 0.5, colour=grey)

    s2[0].add_euclidean_rhythm("Triangle", events=3, steps=6, diameter=diameter * 0.5, freq=freq * 1, colour=YELLOW)
    s3[0].add_euclidean_rhythm("Square", events=4, steps=8, diameter=diameter * 0.5, freq=freq * 1, colour=YELLOW)
    s4[0].add_euclidean_rhythm("Pentagon", events=5, steps=10, diameter=diameter * 0.5, freq=freq * 1, colour=YELLOW)
    rootNode.set_oscillator_speed(0.271)
    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))
    #start paused
    rootNode.set_oscillator_speed(0)
    return rootNode

if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML 2D Euclidean", populate_demo)
    app.initial_rotation_speed(1)
    app.mode_2d=3
    app.run2d()
