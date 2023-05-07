#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../../src/OpenGML") #AddOpenGML path

import GML_App_3D as app3d
from GML import *
from GML_3D import *
from colour_functions import *


def populate_demo(demo_num):
    dia=20 #Size of the singularity drawn
    freq=10 #Determines the size of the circle that the singularities rotate

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu_3D()

    #Add nested polytopes
    polytope_node1 = rootNode.add_cube("Cube", diameter=dia, freq=[freq*10,freq*10], colour=BLUE)
    polytope_node2 = polytope_node1[7].add_tetrahedron("Tetra", diameter=dia/2, freq=[freq * 5, freq * 5], colour=RED)
    polytope_node3 = polytope_node2[0].add_octohedron("Octo", diameter=dia/4, freq=[freq * 2, freq * 2], colour=GREEN)
    #polytope_node4 = polytope_node3[0].add_dodecahedron("Dodeca", diameter=dia/8, freq=[freq * 1, freq * 1], colour=INDIGO)
    #polytope_node5 = polytope_node4[0].add_icosahedron("Isoca", diameter=dia/16, freq=[freq * 0.5, freq * 0.5], colour=YELLOW)

    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))
    return rootNode

if __name__ == '__main__':
    #Run the app
    app=app3d.GML_App_3D("OpenGML Basic Cube",populate_demo)
    app.initial_rotation_speed(0)
    app.run()