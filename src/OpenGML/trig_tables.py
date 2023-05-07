# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 17th June 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Speed up of trigonometry using sine and cosine tables
# =============================================================================

#import numpy as np
import math


sin_array=[]
cos_array=[]
atan_array=[]

TRIG_TABLE_SIZE=16382
DEGREES_INC=TRIG_TABLE_SIZE/360
TWO_PI=2*math.pi
x_min=0
x_max=TWO_PI
x_delta=TWO_PI/TRIG_TABLE_SIZE

atan_min=-100
atan_max=100
atan_range=atan_max-atan_min
atan_delta=atan_range/TRIG_TABLE_SIZE

def frange(start, stop=None, step=None):
    """
    Floating point range s an alternative to numpy np.arange function
    """
    start = float(start)
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
    count = 0
    while True:
        current = float(start + count * step)
        if step > 0 and current >= stop:
            break
        elif step < 0 and current <= stop:
            break
        yield current
        count += 1

def create_tables():
    """
    Populate the trignometric tables
    """
    for x in frange(x_min,x_max,x_delta):
        sin_array.append(math.sin(x))
        cos_array.append(math.cos(x))
    for x in frange(atan_min,atan_max,atan_delta):
        atan_array.append(math.atan(x))

def fast_sin(x):
    """
    Return the fast sine wave using tables
    """
    while(x<0):
        x+=TWO_PI
    while(x>=TWO_PI):
        x-=TWO_PI
    index=int((x/TWO_PI)*TRIG_TABLE_SIZE)
    return sin_array[index]

def fast_cos(x):
    """
    Return the fast cosine wave using tables
    """
    while(x<0):
        x+=TWO_PI
    while(x>=TWO_PI):
        x-=TWO_PI
    index=int((x/TWO_PI)*TRIG_TABLE_SIZE)
    return cos_array[index]

def fast_atan(x):
    """
    Return the fast atan using tables
    """
    x=x-atan_min
    if(x<0):
        x=0
    index=int(x/atan_range*TRIG_TABLE_SIZE)
    if(index>TRIG_TABLE_SIZE-1):
        index=TRIG_TABLE_SIZE-1
    return atan_array[index]


def fast_sin_deg(x):
    """
    Return the fast sine wave (degrees) using tables
    """
    while(x<0):
        x+=360
    while(x>=360):
        x-=360
    index=int(x*DEGREES_INC)
    return sin_array[index]

def fast_cos_deg(x):
    """
    Return the fast cosine wave (degrees) using tables
    """
    while(x<0):
        x+=360
    while(x>=360):
        x-=360
    index=int(x*DEGREES_INC)
    return cos_array[index]

def fast_sqrt(x):
    """
    Return the fast sqrt
    """
    pass

def fast_atan2(y,x):
    """
    Return the fast atan2 using tables
    """
    #return np.arctan2(y,x)
    #return math.atan2(y,x)
    if(x==0):
        if(y==0):
            return 0
        if(y>0):
            return math.pi/2
        else:
            return -math.pi/2
    elif (x>0):
        return fast_atan(y/x)
    elif (y>=0):
        return fast_atan(y/x)+math.pi
    else:
        return fast_atan(y/x)+math.pi
