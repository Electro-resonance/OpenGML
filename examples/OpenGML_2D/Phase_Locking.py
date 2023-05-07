#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 3rd June 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Phase Locking Oscillators
# Example of oscillators that phase lock
# =============================================================================
import sys
sys.path.append("../../src/OpenGML")  # AddOpenGML path

import GML_App_2D as app2d
from GML import *
from GML_3D import *
from GML_Bond import GML_Bond
from colour_functions import * #RGB definitions of Colours
from gl_text_drawing import *
import random


def generate_primes(n):
    """
    Generates primes in the set from 2 to n
    :param n:
    :return:
    """
    primes = []
    for num in range(2, n):
        for i in range(2, num):
            if (num % i) == 0:
                break
        else:
            primes.append(num)
    return primes

def gcd(a, b):
    """
    Returns the greatest common divisor of two integers a and b.
    """
    while b != 0:
        a, b = b, a % b
    return a


def recursive_bonds(singularities, depth, prob=0.5, coupling=0.01):
    """
    Generate bonds between singularities recursively
    :param singularities: singularities (list): List of singularities to generate bonds between.
    :param depth: depth (int): Depth of the recursion.
    :param prob: Probability of a bond being formed at each level of the recursion.
    :return:
    """
    if depth == 0:
        return []
    else:
        bonds = []
        for i in range(len(singularities)):
            for j in range(i + 1, len(singularities)):
                if random.random() < prob:
                    # create a bond between the two singularities
                    bond = GML_Bond(singularities[i], singularities[j], coupling=coupling)
                    bonds.append(bond)

                    # recursively generate bonds between the two sub-groups of singularities
                    midpoint = (singularities[i].phase[0] + singularities[j].phase[0]) / 2
                    left_group = [s for s in singularities if s.phase[0] <= midpoint]
                    right_group = [s for s in singularities if s.phase[0] > midpoint]
                    bonds.extend(recursive_bonds(left_group, depth - 1, prob))
                    bonds.extend(recursive_bonds(right_group, depth - 1, prob))
    return bonds

bonds = []
linkage_enable=True

def populate_demo(demo_num=0):
    """
    Function to create a simple OpenGML tree
    """
    global bonds
    diameter=8 #Size of the singularity drawn
    freq_mult=4 #Determines the size of the circle that the singularities rotate

    colors = [RED, ORANGE, INDIGO, VIOLET, YELLOW]

    primes=generate_primes(20)
    #print(primes)
    #print (gcd(10,25))

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu()

    singularities = []
    # create singularities with frequencies based on prime numbers
    for i in range(len(primes)):
        frequency = primes[i]+80
        # Add a single point to the root node
        offset_angle = random.randint(-180, 180)
        singularity=rootNode.add_singularity(offset_angle, diameter, frequency*freq_mult+50, DARK_GREY)
        singularities.append(singularity[0])
        color = colors[random.randint(0,len(colors)-1)]
        offset_angle=random.randint(-180,180)
        corners = singularity[0].add_triangle(offset_angle, diameter, frequency * freq_mult/2, color)
        for corner in corners:
            singularities.append(corner)
            offset_angle = random.randint(-180, 180)
            corners2=corner.add_square(offset_angle, diameter, frequency * freq_mult/4, color)
            for corner2 in corners2:
                singularities.append(corner2)
                #corners3 = corner2.add_triangle(0, diameter, frequency * freq_mult / 4, color)
                #for corner3 in corners3:
                #    singularities.append(corner3)

    # Create recursive connections between the singularities
    bonds=recursive_bonds(singularities, 1, prob=0.5, coupling=0.0002)

    print("Created bonds=",len(bonds))

    #Print a text version of the tree
    rootNode.print_tree()
    #Print the GML geometry as text
    print("GML geometry text representation: ", rootNode.gml_to_text(100))

    return rootNode

def key_callback(key,dt):
    """
    Callback whenever there is a keypress.
    :param key: the ascii key pressed.
    :param dt: Time in seconds since last key press
    :return:
    """
    global bonds, linkage_enable
    if(dt < 0.02):
        return
    if (key=='w'):
            #Apply bond linkage as a force between singularities
            for bond in bonds:
                bond.update()
    if (key=='e'):
        #Toggle linkage
        linkage_enable=not linkage_enable

def runtime_callback(rootNode):
    """
    Callback which is executed once per runtime cycle after nodes have been updated.
    :param rootNode:
    :return:
    """
    global bonds, linkage_enable
    if(linkage_enable==True):
        # Apply bond linkage as a force between singularities
        for bond in bonds:
            bond.update()


if __name__ == '__main__':
    # Run the app
    app = app2d.GML_App_2D("Phase Locking Oscillators", populate_demo, sonic_enabled=False)
    app.initial_rotation_speed(0.3)
    app.balancing_phases(False)
    app.mode_2d=2
    app.set_depth_projection(False)
    # Add the callbacks
    app.add_key_callback(key_callback)
    app.add_runtime_callback(runtime_callback)
    # Initiate the OpenGML system
    app.run2d()
