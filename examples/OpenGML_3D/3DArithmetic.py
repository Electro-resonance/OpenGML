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
    Function to create a simple OpenGML tree
    """
    diameter=8 #Size of the singularity drawn
    freq=30 #Determines the size of the circle that the singularities rotate

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu_3D()

    s2 = rootNode.add_sphere("Sphere", diameter=diameter, freq=[freq * 5,freq * 5], offset_angle=[1,1], colour=GREEN)
    rootNode.add_singularity([0, 0], diameter=diameter, freq=[freq * 5, freq * 5], colour=MAGENTA)

    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML Arithmetic", populate_demo)
    app.initial_rotation_speed(0.671)
    app.balancing_phases(True)
    app.set_zoom_relative(-3) #Zoom out
    app.run()