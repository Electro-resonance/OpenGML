#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 3rd June 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Prime Linkages
# Add phase linkages between singularities as one step towards a Self Organising
# Mathematical Universe (SOMU) in which the interactions between singularities become
# generative. Demonstrated using a set of circles representing a subset of the
# prime numbers.
# =============================================================================
import sys
sys.path.append("../../src/OpenGML")  # AddOpenGML path

import GML_App_2D as app2d
from GML import *
from GML_3D import *
from GML_Bond import GML_Bond
from colour_functions import * #RGB definitions of Colours
from prime_functions import * #Prime number functions
from gl_text_drawing import *

bonds = []
linkage_enable=True

def populate_demo(demo_num=0):
    """
    Function to create a simple OpenGML tree
    """
    global bonds
    diameter=8 #Size of the singularity drawn
    freq_mult=4 #Determines the size of the circle that the singularities rotate


    primes=generate_primes(100)
    #print(primes)
    #print (gcd(10,25))

    #Create a tiny point as starting root node for the GML tree
    rootNode=create_bindu()

    singularities = []
    # create singularities with frequencies based on prime numbers
    for i in range(len(primes)):
        frequency = primes[i]
        # Add a single point to the root node
        singularity=rootNode.add_singularity(0, diameter, frequency*freq_mult, RED)
        singularities.append(singularity[0])

    # create bonds based on relationships between frequencies
    for i in range(len(singularities)):
        for j in range(i + 1, len(singularities)):
            frequency_i = int((singularities[i].freq)[0]/freq_mult)
            frequency_j = int((singularities[j].freq)[0]/freq_mult)
            print(frequency_i,frequency_j)
            if frequency_i != frequency_j and gcd(frequency_i, frequency_j) == 1:
                bond = GML_Bond(singularities[i], singularities[j], coupling=0.0005)
                bonds.append(bond)

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
    app = app2d.GML_App_2D("Prime numbers and GML Linkages", populate_demo, sonic_enabled=False)
    app.initial_rotation_speed(0.3)
    app.balancing_phases(False)
    app.mode_2d=3
    app.set_depth_projection(False)
    # Add the callbacks
    app.add_key_callback(key_callback)
    app.add_runtime_callback(runtime_callback)
    # Initiate the OpenGML system
    app.run2d()
