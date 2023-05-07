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

    #s2 = rootNode.add_cube(0,   diameter*1.3, [freq*2.3,freq*2.3], CYAN)
    s2 = rootNode.add_fibonaaci_sphere("Fibonnaci", samples=100, diameter=diameter*1.3, freq=[freq*2.3,freq*2.3], colour=CYAN, offset_angle=[0,0], swap_axis=False)
    s3=s2[70].add_fibonaaci_sphere("Fibonnaci", samples=10, diameter=diameter*0.7, freq=[freq*1.3,freq*1.3], colour=RED, offset_angle=[0,0], swap_axis=False)
    s4=s2[5].add_fibonaaci_sphere("Fibonnaci", samples=11, diameter=diameter*0.2, freq=[freq*1.6,freq*1.6], colour=GREEN, offset_angle=[0,0], swap_axis=False)
    s5=s4[5].add_fibonaaci_sphere("Fibonnaci", samples=12, diameter=diameter*0.5, freq=[freq*1.0,freq*1.0], colour=YELLOW, offset_angle=[0,0], swap_axis=True)
    s6=s5[5].add_fibonaaci_sphere("Fibonnaci", samples=13, diameter=diameter*0.2, freq=[freq*1.5,freq*1.5], colour=CYAN, offset_angle=[0,0], swap_axis=False)
    s7=s6[5].add_fibonaaci_sphere("Fibonnaci", samples=14, diameter=diameter*0.3, freq=[freq*1.0,freq*1.0], colour=GREY1, offset_angle=[0,0], swap_axis=False)
    s8=s7[5].add_fibonaaci_sphere("Fibonnaci", samples=6, diameter=diameter*0.2, freq=[freq*1.1,freq*1.1], colour=BLUE, offset_angle=[0,0], swap_axis=False)
    s9=s8[5].add_fibonaaci_sphere("Fibonnaci", samples=15, diameter=diameter*1, freq=[freq*1.0,freq*1.0], colour=MAGENTA, offset_angle=[0,0], swap_axis=False)
    s10=s9[5].add_fibonaaci_sphere("Fibonnaci", samples=3, diameter=diameter*0.1, freq=[freq*0.5,freq*0.5], colour=FLGREEN, offset_angle=[90,0], swap_axis=False)

    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))
    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML Polyhedron Example", populate_demo)
    app.initial_rotation_speed(0.671)
    app.set_zoom_relative(-4) #Zoom out
    app.run()