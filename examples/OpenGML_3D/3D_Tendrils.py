#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("../../src/OpenGML")  # AddOpenGML path

import GML_App_3D as app3d
from GML import *
from GML_3D import *
from colour_functions import *
import random


def populate_demo(demo_num):
    """
    Function to create a simple OpenGML tree
    """
    diameter=8 #Size of the singularity drawn
    freq=40 #Determines the size of the circle that the singularities rotate

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu_3D()
    s2 = rootNode.add_cube("Cube", diameter=diameter*1.3, freq=[freq*1.3,freq*1.3], colour=CYAN, offset_angle=[0,0],
                           rotation_matrix=np.array([[0,1,0,0],[0,0,0,1]]))
    s3 = s2[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])
    s4 = s3[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])
    s5 = s4[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])
    s6 = s5[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])
    s7 = s6[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])
    s8 = s7[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])
    s9 = s8[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])
    s10 = s9[5].add_cube("Cube", diameter=diameter * 0.7, freq=[freq * 0.7, freq * 0.7], colour=GREEN,
                            offset_angle=[0, 0])

    arm_length=15
    leg_length=20

    tendril1=[]
    tendril1.append(s10)
    for i in range(0,leg_length):
        side=random.randint(4,6)
        tendril1.append((tendril1[i])[side].add_cube("Cube", diameter=diameter * 0.1, freq=[freq * .3, freq * .3], colour=RED,
                            offset_angle=[0, 0])  )

    tendril1[leg_length-1][1].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 0.6, freq * 0.6], colour=MAGENTA,
                            offset_angle=[0, 0])

    tendril2=[]
    tendril2.append(s10)
    for i in range(0,leg_length):
        side=random.randint(1,3)
        tendril2.append((tendril2[i])[side].add_cube("Cube", diameter=diameter * 0.1, freq=[freq * .3, freq * .3], colour=RED,
                            offset_angle=[0, 0])  )
    tendril2[leg_length-1][1].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 0.6, freq * 0.6], colour=MAGENTA,
                            offset_angle=[0, 0])

    tendril3=[]
    tendril3.append(s4)
    for i in range(0,arm_length):
        side=random.randint(1,7)
        tendril3.append((tendril3[i])[side].add_cube("Cube", diameter=diameter * 0.1, freq=[freq * .3, freq * .3], colour=BLUE,
                            offset_angle=[0, 0])  )
    tendril3[arm_length-1][1].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 0.6, freq * 0.6], colour=GREEN,
                            offset_angle=[0, 0])

    tendril4=[]
    tendril4.append(s4)
    for i in range(0,arm_length):
        side=random.randint(4,6)
        tendril4.append((tendril4[i])[side].add_cube("Cube", diameter=diameter * 0.1, freq=[freq * .3, freq * .3], colour=BLUE,
                            offset_angle=[0, 0])  )
    tendril4[arm_length-1][1].add_cube("Cube", diameter=diameter * 1.3, freq=[freq * 0.6, freq * 0.6], colour=GREEN,
                            offset_angle=[0, 0])

    rootNode.print_tree()
    print("GML geometry text representation: ", rootNode.gml_to_text(100))

    return rootNode


if __name__ == '__main__':
    # Run the app
    app = app3d.GML_App_3D("OpenGML Tendrils", populate_demo)
    app.initial_rotation_speed(0.3)
    app.balancing_phases(True)
    app.set_graphics_mode(0) # Disable surfaces
    app.set_zoom_relative(-5) #Zoom out
    app.run()