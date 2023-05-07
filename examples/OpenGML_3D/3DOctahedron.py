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

    s2 = rootNode.add_octohedron("Octohedron", diameter=diameter*1.3, freq=[freq*5.3,freq*1.3], colour=CYAN)
    s3 = s2[0].add_octohedron("Octohedron", diameter=diameter * 1.3, freq=[freq * 1.7, freq * 1.9], colour=FLGREEN,
                            offset_angle=[0, 0])
    s4 = s2[1].add_octohedron("Octohedron", diameter=diameter * 1.3, freq=[freq * 1.7, freq * 1.9], colour=BLUE,
                            offset_angle=[0, 0])
    s5 = s2[2].add_octohedron("Octohedron", diameter=diameter * 1.3, freq=[freq * 1.7, freq * 1.9], colour=MAGENTA,
                            offset_angle=[0, 0])
    s6 = s2[3].add_octohedron("Octohedron", diameter=diameter * 1.3, freq=[freq * 1.7, freq * 1.9], colour=GREEN,
                            offset_angle=[0, 0])
    s7 = s2[4].add_octohedron("Octohedron", diameter=diameter * 1.3, freq=[freq * 1.7, freq * 1.9], colour=YELLOW,
                            offset_angle=[0, 0])
    s8 = s2[5].add_octohedron("Octohedron", diameter=diameter * 1.3, freq=[freq * 1.7, freq * 1.9], colour=YELLOW,
                            offset_angle=[0, 0])

    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))
    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML ChatGPT Example", populate_demo)
    app.initial_rotation_speed(0.371)
    app.set_zoom_relative(-3) #Zoom out
    app.run()