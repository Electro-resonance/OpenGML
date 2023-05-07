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
    Function to create a triplet of triplet
    Reconstructs Figure 6.4 (a) P154,
    "NANOBRAIN The Making of an Artificial Brain from a Time Crystal" by Anirban Bandyopadhyay
    """
    dia=0.001 #Size of the singularity drawn
    freq=10 #Determines the size of the circle that the singularities rotate

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu_3D()

    #Base layer triplet
    triplet1_nodes=rootNode.add_triangle([0,0], diameter=dia, freq=[freq*7,freq*7], colour=RED)
    # Add triplet of triplet with 8 singularities on the outer layer
    for second_triplet in triplet1_nodes:
        triplet2_nodes=second_triplet.add_triangle([0,0], diameter=dia, freq=[freq*3.5,freq*3.5], colour=GREEN)
        for mid_triplet in triplet2_nodes:
            outer_nodes=mid_triplet.add_cube("Cube", diameter=dia, freq=[freq*1,freq*1], colour=BLUE)
            for outer in outer_nodes:
                outer.add_singularity([0,0], diameter=dia, freq=[freq * 0.2, freq * 0.2], colour=MAGENTA)

    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))
    return rootNode

if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML ChatGPT Example", populate_demo)
    app.initial_rotation_speed(0.2)
    app.run()