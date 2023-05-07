#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 18th June 2022
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
import random

def populate_demo(demo_num):
    """
    For a given demo number construct the GML tree for that demo
    """
    diameter = 8
    freq = 30
    if(demo_num == 0):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Fast construction of reducing nested polygons
        #Creates 73 nested clocks
        rootNode.add_polygon(
            "ReducingPoly", 4, 0, diameter*1.5, freq*7, CYAN, 3, 0.5, -2, +1, True, True)
    elif(demo_num == 1):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Fast construction of reducing nested polygons
        #With a 1-9 counting pattern
        #creating 289 oscillators from one command
        rootNode.add_polygon("ReducingPoly", 9, 0, diameter
                             * 1.5, freq*10, MAGENTA, 3, 0.1, -1, -1, True, True)
    elif(demo_num == 2):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Arrangement of five nested polygons of different types
        #289 oscillators
        rootNode.add_polygon("NestedPoly5", 5, 0,
                             diameter*1.3, freq*8, CYAN, 3, 0.5, -4)
        subNode1 = rootNode.nth_child()
        subNode1.add_polygon("NestedPoly6", 6, 0,
                             diameter*1.4, freq*2, MAGENTA, 3, 0.4, -2)
        subNode2 = rootNode.nth_child(1)
        subNode2.add_polygon("NestedPoly4", 4, 0,
                             diameter*1, freq*1.8, YELLOW, 3, 0.6, -3)
        subNode3 = rootNode.nth_child(3)
        subNode3.add_polygon("NestedPoly7", 7, 0,
                             diameter*1, freq*1.5, BLUE_PURPLE, 3, 0.6, -2)
        subNode4 = rootNode.nth_child(4)
        subNode4.add_polygon("NestedPoly9", 9, 0,
                             diameter*1, freq*1.3, VIOLET, 3, 0.3, -5)
    elif(demo_num == 3):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Demo with simple named geometries built using several commands
        rootNode.add_triangle(0, diameter*2, freq*2, BLUE_PURPLE, 1, 0.1)
        subNode1 = rootNode.nth_child()
        subNode1.add_square(0,   diameter,   freq*3,
                            MAGENTA, 1, 0.3)  # Nested 2 deep
        subNode2 = rootNode.nth_child()
        subNode2.add_heptagon(0, diameter,   freq*6,
                              YELLOW, 2, 0.2)  # Nested 3 deep
        subNode3 = subNode1.nth_child()
        subNode3.add_triangle(0, diameter*2, freq*2,
                              CYAN, 1, 0.1)  # Nested 2 deep
        subNode3.add_pentagon(0, diameter,   freq*5,   RED)
        #subNode2.add_child(rootNode)
    elif(demo_num == 4):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #named geometries with larger diameter singularity circles
        #Phasing creates outlines similar to the human outline
        #with head, arms and legs
        rootNode.add_singularity(0, diameter*1, freq*2, RED)
        rootNode.add_dipole(0, diameter*2, freq*4, MAGENTA)
        rootNode.add_triangle(0, diameter*3, freq*6, YELLOW)
        rootNode.add_square(0,   diameter*4,   freq*8, CYAN)
        rootNode.add_pentagon(0, diameter*5,   freq*10, BLUE_PURPLE)
    elif(demo_num == 5):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #A nested polygon with two end spurs
        rootNode.add_polygon_list("PolyList", [
                                  3, 3, 1, 1, 1, 0, 1, 0, 1, 0, 2, 4, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0], 0, diameter*1, freq*6, MAGENTA, 0.5, True)
    elif(demo_num == 6):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #A nested polygon with two end spurs
        rootNode.add_polygon_list("PolyList", [
                                  1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0], 0, diameter*1, freq*4, YELLOW, 0.8, True)
    elif(demo_num == 7):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Generalised Neuron implementing Figure 6.14 of "NanoBrain The Making of an Artificial Brain from a Time Crystal" by Anirban Bandyopadhyay.
        rootNode.add_polygon_list("Neuron",
                                  [3,
                                   4, 3, 1, 0, 1, 0, 1, 0, 4, 1, 0, 1, 0, 1, 0, 1, 0, 3, 1, 0, 1, 0, 1, 0, 2, 1, 0, 3, 1, 0, 1, 0, 1, 0,
                                   4, 2, 1, 0, 1, 0, 2, 1, 0, 1, 0, 4, 1, 0, 1, 0, 1, 0, 1, 0, 3, 1, 0, 1, 0, 1, 0,
                                   4, 1, 0, 1, 0, 1, 0, 3, 3, 1, 0, 1, 0, 1, 0, 3, 1, 0, 1, 0, 1, 0, 2, 1, 0, 3, 1, 0, 1, 0, 2, 1, 0, 3, 1, 0, 1, 0, 1, 0],
                                  0, diameter*1, freq*7, CYAN, 0.5, True)
    elif(demo_num == 8):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Demo with a list of polygons defining two tentacle nested structures
        rootNode.add_polygon_list("PolyList", [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,
                                  1, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0], 0, diameter*1, freq*4, YELLOW, 0.8, True)

    elif(demo_num == 9):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #demno with lots of spirals connected to a hexhagon.
        #f=rootNode.add_angle(0, diameter*1, freq*3, colour7, 2,0,60)
        #f.add_corner(0, diameter*1, freq*4, colour7, 2,1)
        spirality = 1
        rootNode.add_hexagon(0, diameter*1.1, freq*14, RED, 1, 0.1)
        subNode2 = rootNode.nth_child(0)
        subNode3 = rootNode.nth_child(1)
        subNode4 = rootNode.nth_child(2)
        subNode5 = rootNode.nth_child(3)
        subNode6 = rootNode.nth_child(4)
        subNode7 = rootNode.nth_child(5)

        s1 = rootNode.add_spiral(
            0, diameter*3, freq*4, BLUE_PURPLE, spirality*2, 2, 2)
        #rootNode.add_spiral(0, diameter*1, freq*2, colour6, spirality*2,1)
        #n1=rootNode.add_spiral(0, diameter*1, freq*8, RED, spirality*3,1)
        n2 = subNode2.add_spiral(
            0, diameter*1.5, freq*4, MAGENTA, spirality*2, 1, 0)
        n3 = subNode3.add_spiral(
            0, diameter*1.5, freq*4, YELLOW, spirality*-1, 1, 0)
        n4 = subNode4.add_spiral(
            0, diameter*1.5, freq*4, CYAN, spirality*9, 4, -9)
        n5 = subNode5.add_spiral(
            0, diameter*1.5, freq*4, BLUE_PURPLE, spirality*-3, 4, 0)
        n6 = subNode6.add_spiral(
            0, diameter*1.5, freq*4, VIOLET, spirality*7, 1, 1)
        n7 = subNode7.add_spiral(
            0, diameter * 1.5, freq * 4, SEABLUE, spirality * 2, 3, 1)

        nn2 = n7.add_pentagon(0, diameter*1.1, freq*2, RED, 1, 0.1)
        subNode8 = nn2[1]
        nn3 = subNode8.add_triangle(
            0, diameter*1.4, freq*1.6, MAGENTA, 1, 0.1)

        n3.add_spiral(0, diameter*1.5, freq*1.4,
                      CYAN, spirality*5.7, 4, 0)

        nn1 = n5.add_spiral(0, diameter * 1.5, freq * 3,
                            SEABLUE, spirality * 0.5, 1, 0)

    elif(demo_num == 10):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Demo with angle and corner oscillators
        s0 = rootNode.add_singularity(0, diameter*1, freq*4, RED)
        n1 = rootNode.nth_child(0)
        n2 = n1.add_angle(0, diameter*1, freq*8, MAGENTA, 2, 2, 60)
        n3 = n2.add_corner(0, diameter*1, freq*6, YELLOW, 2, 0)
        n4 = n3.add_angle(0, diameter*1, freq*4, CYAN, 2, 2, 10)
        n5 = n4.add_spiral(0, diameter*1.5, freq*2, BLUE_PURPLE, 2, 2, 2)

    elif(demo_num == 11):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Nested spirals of different types with complex motions
        spirality = 1
        s0 = rootNode.add_singularity(0, diameter * 2, freq * 6, SEABLUE)
        s1 = rootNode.nth_child(0)
        s2 = s1.add_spiral(0, diameter*2, freq*4,
                           BLUE_PURPLE, spirality*2, 3, 2)
        t2 = s2.add_spiral(0, diameter*2, freq*5,
                           RED, spirality*2, 3, -2)
        t3 = t2.add_spiral(0, diameter*2, freq*4,
                           MAGENTA, spirality*2, 3, -2)
        t4 = t3.add_spiral(0, diameter*2, freq*3,
                           YELLOW, spirality*2, 3, -2)
        t5 = t4.add_spiral(0, diameter*2, freq*2,
                           CYAN, spirality*2, 3, -2)
        t6 = t5.add_spiral(0, diameter*2, freq*1,
                           BLUE_PURPLE, spirality*2, 3, -2)
        t6.add_triangle(0, diameter*1, freq*5, RED)
        n1 = t6.nth_child(0)
        n2 = t6.nth_child(1)
        n3 = t6.nth_child(2)
        n4 = n1.add_spiral(0, diameter*4, freq*4,
                           VIOLET, spirality*9, 4, -1)
        n5 = n2.add_spiral(0, diameter * 4, freq * 4,
                           SEABLUE, spirality * -9, 4, -1)
        n6 = n3.add_spiral(0, diameter*4, freq*4,
                           FLGREEN, spirality*9, 4, 1)

    elif(demo_num == 12):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Three nested large spirals Creating colour overlap moire patterns
        spirality = 1
        n1 = rootNode.add_spiral(
            0, diameter*2, freq*9, RED, spirality*27, 2, -1)
        n2 = n1.add_spiral(0, diameter * 2, freq * 8.5,
                           SEABLUE, spirality * 26, 2, 1)
        n3 = n2.add_spiral(0, diameter*2, freq*8.75,
                           BLUE, spirality*25, 2, -1)

    elif(demo_num == 13):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #Nested Pendulums
        rootNode.add_pentagon(0, diameter*1.1, freq*10, RED, 1, 0.1)
        subNode1 = rootNode.nth_child(0)
        subNode2 = rootNode.nth_child(1)
        subNode3 = rootNode.nth_child(2)
        subNode4 = rootNode.nth_child(3)
        subNode5 = rootNode.nth_child(4)

        n6 = rootNode.add_pendulum(0, diameter * 1, freq * 3, SEABLUE, 0, 2)
        n7 = n6.add_pendulum(0, diameter*1, freq*2, FLGREEN, 1, 2)
        n8 = n7.add_pendulum(0, diameter*1, freq*1, CYAN, 2, 2)

        n1 = subNode1.add_linear(0, diameter*1, freq*6, MAGENTA, 0, 1)
        n2 = subNode2.add_linear(0, diameter*1, freq*6, YELLOW, 1, 2)
        n3 = subNode3.add_linear(0, diameter*1, freq*6, CYAN, 2, 4)
        n4 = subNode4.add_linear(0, diameter*1, freq*6, BLUE_PURPLE, 3, 8)
        n5 = subNode5.add_linear(0, diameter*1, freq*6, VIOLET, 4, 16)

    elif(demo_num == 14):
        #Define the centre of the GML as the root node
        rootNode = create_bindu()
        #named geometries with larger diameter singularity circles
        #Phasing creates outlines similar to the human outline
        #with head, arms and legs
        tri1 = rootNode.add_triangle(0, diameter*1, freq*5.5, RED)
        tri11 = tri1[0].add_triangle(0, diameter*2, freq*5.7, MAGENTA)
        tri12 = tri1[1].add_triangle(0, diameter*2, freq*5.9, MAGENTA)
        tri13 = tri1[2].add_triangle(0, diameter*2, freq*6.2, MAGENTA)
        tri111 = tri11[0].add_triangle(0, diameter*2, freq*1, YELLOW)
        tri112 = tri11[1].add_triangle(0, diameter*2, freq*2, CYAN)
        tri113 = tri11[2].add_triangle(0, diameter*2, freq*3, BLUE_PURPLE)
        tri211 = tri12[0].add_triangle(0, diameter*2, freq*4, YELLOW)
        tri212 = tri12[1].add_triangle(0, diameter*2, freq*5, CYAN)
        tri213 = tri12[2].add_triangle(0, diameter*2, freq*6, BLUE_PURPLE)
        tri311 = tri13[0].add_triangle(0, diameter*2, freq*7, YELLOW)
        tri312 = tri13[1].add_triangle(0, diameter*2, freq*8, CYAN)
        tri313 = tri13[2].add_triangle(0, diameter*2, freq*9, BLUE_PURPLE)

    rootNode.set_oscillator_speed(1.71)
    rootNode.set_oscillator_speed(0.5)
    if(demo_num == 12):
        rootNode.set_oscillator_speed(0.05)
    return rootNode

def demo_callback(app,demo_num):
    if (demo_num == 6 or demo_num >= 8 or demo_num == 0):
        # Show an X and Y sideways projection of the GML tree as a set of
        # circular nodes in left hand and lower edge of the screen
        for depth in range(1, 20):
            app.rootNode.depth_projection(
                depth, [0, 255, 0], depth * 10, True)
            app.rootNode.depth_projection(
                depth, [255, 0, 0], depth * 10, False)
            app.rootNode.depth_projection(
                depth, [255, 0, 0], depth * 10, False)


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("OpenGML Demo", populate_demo)
    app.initial_rotation_speed(1)
    app.balancing_phases(False)
    app.mode_2d=3
    app.set_depth_projection(False)
    app.add_demo_num_callback(demo_callback)
    app.run2d()