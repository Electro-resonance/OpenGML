# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 22nd March 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Midi abstraction class
# =============================================================================


import pygame
from pygame.locals import *
import pygame.midi

GRAND_PIANO = 0
instrument = 9
C = 74
MAX = 127

def midi_init():
    """
    Initialise Midi functions
    """
    global midi_out, port
    pygame.midi.init()
    port = pygame.midi.get_default_output_id()
    midi_out = pygame.midi.Output(port, 0)
    midi_out.set_instrument(instrument, 0)
    print("using output_id :%s:" % port)

def midi_quit():
    """
    Function to close Midi channel on exit
    """
    global midi_out
    music = 0
    del midi_out
    pygame.midi.quit()
    pygame.quit()


def all_midi_off():
    """
    Stop all midi notes
    """
    for note in range(0,127):
        midi_out.note_on(note, 0)
    pygame.time.delay(10)
    for note in range(0,127):
        midi_out.note_off(note, 0)
    pygame.time.delay(10)
    for note in range(0,127):
        midi_out.note_off(note, 0)

def midi_on(notes_in=[C], vol=[MAX]):
    """
    Trigger an external midi note
    """
    note = list(dict.fromkeys(notes_in)) #remove duplicates
    i = 0
    for n in note:
        no = int(n)
        volume = int(127-vol[i]*4)
        if(volume < 0):
            volume = 0
        #print(n)
        if(n > 0):
            # 74 is middle C, 127 is "how loud" - max is 127
            midi_out.note_on(no, volume)
        i += 1

def midi_off(note=[C], note2=[C], volume=MAX):
    """
    Disable an external midi note
    """
    if (note != None):
        for n in note:
            no = int(n)
            #Check for notes that should not be off
            for n1 in note2:
                if(no == int(n1)):
                    #Flag as not to clear
                    n = 0
            if(n > 0):
                midi_out.note_off(no, 0)
