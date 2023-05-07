#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
#sudo easy_install-3.7 anytree

#https://anytree.readthedocs.io/en/latest/

import sys
sys.path.append("../../src/OpenGML") #AddOpenGML path

from anytree import NodeMixin, RenderTree
import math
import GML_App_3D as app3d

from OpenGL.GL import *
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
    s2 = rootNode.add_cube("Cube", diameter=diameter*1.3, freq=[freq*5.3,freq*1.3], colour=CYAN, offset_angle=[0,0],
                           rotation_matrix=np.array([[0,1,0,0],[0,0,0,1]]))
    s3 = s2[7].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=FLGREEN,
                            offset_angle=[0, 0])
    s4 = s2[0].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 0.6, freq * 0.6], colour=BLUE,
                            offset_angle=[0, 0])
    s5 = s2[6].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 2.3, freq * 2.5], colour=MAGENTA,
                            offset_angle=[0, 0])
    s6 = s5[6].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 0.8, freq * 1.3], colour=GREEN,
                            offset_angle=[0, 0])
    s7 = s2[1].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 1.7, freq * 1.9], colour=YELLOW,
                            offset_angle=[0, 0])
    s8=s2[4].add_fibonaaci_sphere("Fibonnaci", samples=73, diameter=diameter*1, freq=[freq*1.7,freq*1.7], colour=VIOLET, offset_angle=[90,0], swap_axis=False)

    s9=s2[5].add_fibonaaci_sphere("Fibonnaci", samples=21, diameter=diameter*1, freq=[freq*0.7,freq*0.7], colour=BLUE, offset_angle=[90,0], swap_axis=False)


    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))
    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML Nested Polyhedra", populate_demo)
    app.initial_rotation_speed(0)
    app.set_graphics_mode(0) # Disable surfaces
    app.set_zoom_relative(-2 ) #Zoom in
    app.run()