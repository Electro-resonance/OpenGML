# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 22nd March 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Helper functions for PyGame colours
# =============================================================================

from random import randint

BLACK = (0, 0, 0)
WHITE = [255, 255, 255]
GREY = [127, 127, 127]
GREY1 = [127, 127, 127]
GREY2 = [155, 155, 155]
GREY3 = (200, 200, 200)
DARK_GREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = [255, 0, 255]
YELLOW = [255, 255, 0]
CYAN = [0, 255, 255]
PART_RED = [255, 0, 127]
PART_YELLOW = [255, 127, 0]
PART_CYAN = [0, 255, 127]
BLUE_PURPLE = [200, 200, 255]
ORANGE = [255,165,0]
VIOLET = [190, 100, 155]
SEABLUE = [0, 255, 190]
FLGREEN = [190, 255, 0]
GREEN2 = [30, 255, 105]
INDIGO = [75, 0, 130]

def subtractColours (colour1,colour2,wrap):
    """
    Generate a colour as a difference of two supplied colours
    """
    new_colour=[0,0,0]
    for i in range(0,2):
        new_colour[i]=colour1[i]+colour2[i]
        if (new_colour[i]>255):
            new_colour[i]=wrap
        if(new_colour[i]<0):
            new_colour[i]=255
    return new_colour

def saturateColour(colour1,sat):
    """
    Generate a colour which is more intense
    """
    new_colour=[0,0,0,255]
    for ind in range(0,3):
        if(new_colour[ind]>127):
            new_colour[ind]=int((colour1[ind]+10)*sat)
        else:
            new_colour[ind]=int((colour1[ind]-4)/sat)
        if (new_colour[ind]>255):
            new_colour[ind]=255
        elif (new_colour[ind]<40):
            new_colour[ind]=40
    return new_colour

def randColour(min,max):
    """
    Return a random colour
    """
    return [randint(min[0],max[0]),randint(min[1],max[1]),randint(min[2],max[2])]
