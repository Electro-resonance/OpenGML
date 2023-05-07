#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("../../src/OpenGML")  # AddOpenGML path

import GML_App_3D as app3d
from GML import *
from GML_3D import *
from colour_functions import *


def populate_demo(demo_num):
    # Size of the singularities drawn
    diameter = 20
    # Frequency determines the size of the circle that the singularities rotate
    frequency = [100, 100]

    # Create the Bindu - a tiny point as starting root node for the GML tree
    rootNode = create_bindu_3D()

    # Add a cube
    rootNode.add_cube("Cube", diameter, frequency, colour=BLUE)

    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))
    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML Basic Cube", populate_demo)
    app.initial_rotation_speed(0)
    app.run()
