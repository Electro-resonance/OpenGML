# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 22nd March 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Midi abstraction class
# =============================================================================


import os
fluid_path=os.path.dirname(__file__)+'\\..\\..\\3rdParty\\'
os.environ['PATH'] += r';'+fluid_path #Path for FluidSynth library
print('FluidSynth library path:',fluid_path)
import ctypes
from ctypes.util import find_library
lib = find_library('libfluidsynth-3')
print("Path found to libfluidsynth-3 :",lib)


from kivy.clock import Clock
from functools import partial
import fluidsynth
import time
import logging

C = 74
MAX = 127
fs = None
sfid = None
midi_channels = 64
instruments = None

instrument_list = ['Acoustic Grand Piano', 'Bright Acoustic Piano', 'Electric Grand Piano', 'Honky-tonk Piano', 'Electric Piano 1', 'Electric Piano 2', 'Harpsichord', 'Clavinet',
                   'Celesta', 'Glockenspiel', 'Music Box', 'Vibraphone', 'Marimba', 'Xylophone', 'Tubular Bells', 'Dulcimer',
                   'Drawbar Organ', 'Percussive Organ', 'Rock Organ', 'Church Organ', 'Reed Organ', 'Accordion', 'Harmonica', 'Tango Accordion',
                   'Acoustic Guitar (nylon)', 'Acoustic Guitar (steel)', 'Electric Guitar (jazz)', 'Electric Guitar (clean)', 'Electric Guitar (muted)', 'Overdriven Guitar', 'Distortion Guitar', 'Guitar Harmonics',
                   'Acoustic Bass', 'Electric Bass (finger)', 'Electric Bass (pick)', 'Fretless Bass', 'Slap Bass 1', 'Slap Bass 2', 'Synth Bass 1', 'Synth Bass 2',
                   'Violin', 'Viola', 'Cello', 'Contrabass', 'Tremolo Strings', 'Pizzicato Strings', 'Orchestral Harp', 'Timpani',
                   'String Ensemble 1', 'String Ensemble 2', 'Synth Strings 1', 'Synth Strings 2', 'Choir Aahs', 'Voice Oohs', 'Synth Choir', 'Orchestra Hit',
                   'Trumpet', 'Trombone', 'Tuba', 'Muted Trumpet', 'French Horn', 'Brass Section', 'Synth Brass 1', 'Synth Brass 2',
                   'Soprano Sax', 'Alto Sax', 'Tenor Sax', 'Baritone Sax', 'Oboe', 'English Horn', 'Bassoon', 'Clarinet',
                   'Piccolo', 'Flute', 'Recorder', 'Pan Flute', 'Blown Bottle', 'Shakuhachi', 'Whistle', 'Ocarina',
                   'Lead 1 (square)', 'Lead 2 (sawtooth)', 'Lead 3 (calliope)', 'Lead 4 (chiff)', 'Lead 5 (charang)', 'Lead 6 (voice)', 'Lead 7 (fifths)', 'Lead 8 (bass + lead)',
                   'Pad 1 (new age)', 'Pad 2 (warm)', 'Pad 3 (polysynth)', 'Pad 4 (choir)', 'Pad 5 (bowed)', 'Pad 6 (metallic)', 'Pad 7 (halo)', 'Pad 8 (sweep)',
                   'FX 1 (rain)', 'FX 2 (soundtrack)', 'FX 3 (crystal)', 'FX 4 (atmosphere)', 'FX 5 (brightness)', 'FX 6 (goblins)', 'FX 7 (echoes)', 'FX 8 (sci-fi)',
                   'Sitar', 'Banjo', 'Shamisen', 'Koto', 'Kalimba', 'Bagpipe', 'Fiddle', 'Shanai',
                   'Tinkle Bell', 'Agogo', 'Steel Drums', 'Woodblock', 'Taiko Drum', 'Melodic Tom', 'Synth Drum', 'Reverse Cymbal',
                   'Guitar Fret Noise', 'Breath Noise', 'Seashore', 'Bird Tweet', 'Telephone Ring', 'Helicopter', 'Applause', 'Gunshot']


def midi_init():
    """
    Initialise Midi functions
    """
    global port, fs, sfid, instruments, midi_channels
    port = 0
    fs = fluidsynth.Synth()
    if fs is not None:
        #fs.start(driver='coreaudio') #Mac
        #fs.system_reset()
        #fs.start()
        #fs.delete()
        #fs = fluidsynth.Synth()
        #time.sleep(1)
        #fs.start()
        #sfid = fs.sfload("Sinfon36Plus.sf2")

        #https://member.keymusician.com/Member/FluidR3_GM/index.html
        sfid = fs.sfload(fluid_path+'FluidR3_GM.sf2')
        #sfid = fs.sfload("GM.sf2")
        #sfid = fs.sfload("alex_gm.sf2")
        #sfid = fs.sfload("2MBGMGS.SF2")
        #https://musescore.org/en/node/109371
        #sfid = fs.sfload("OmegaGMGS2.sf2")
        fs.start()
        time.sleep(1)

        #instruments=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        #instruments=[49,46,15,25,69,42,74,0,7,43,41,47,72,77,72,7,49,11,12,25,70,63,75,1,9,25,42,48,73,69,69,0,46,15,25,69,57,74,8,0,47,47,0,47,0,47,0,47,0,47,0,47,0,47,0,47,0,47,0,0,0,0,0,0]
        #instruments = [49, 46, 14, 25, 69, 42, 74, 0, 7, 43, 41, 71, 72, 77, 72, 7, 49, 11, 12, 25, 70, 74, 75, 1, 9, 25, 42, 48, 71, 69, 69, 0, 46, 13, 25, 69, 57, 60, 8, 0, 61, 46, 73, 74, 0, 33, 0, 65, 73, 66, 0, 67, 0, 68, 74, 69, 0, 70, 0, 0, 0, 73, 0, 74]
        instruments = [75, 75, 75, 71, 72, 76, 77, 78,75, 75, 75, 71, 72, 76, 77, 78,75, 75, 75, 71, 72, 76, 77, 78]
        #instruments = [49, 46, 14, 25, 69, 42, 74, 75, 7, 43, 41, 71, 72, 77, 72, 7, 49, 11, 12, 25, 70, 74, 75, 72, 9, 25, 42, 48, 71, 69, 69, 75, 46, 13, 25, 69, 57, 60, 8, 71, 61, 46, 73, 74, 76, 33, 77, 65, 73, 66, 77, 67, 76, 68, 74, 69, 78, 70, 78, 72, 71, 73, 78, 74]
        #instruments = [1]
        chan = 0
        for instr in instruments:
            fs.program_select(chan, sfid, 0, instr)
            chan += 1
        midi_channels = chan
        #print("MIDI Channels:",chan)
        logging.info("[MIDI        ] "+str(chan)+" channels enabled")
        # fs.program_select(0, sfid, 0, 49)
        # fs.program_select(1, sfid, 0, 46)
        # fs.program_select(2, sfid, 0, 15)
        # fs.program_select(3, sfid, 0, 25)
        # fs.program_select(4, sfid, 0, 69)
        # fs.program_select(5, sfid, 0, 57) #62
        # fs.program_select(6, sfid, 0, 74)
        # fs.program_select(7, sfid, 0, 0)
        #
        # fs.program_select(8, sfid, 0, 7)
        # fs.program_select(9, sfid, 0, 43)
        # fs.program_select(10, sfid, 0, 41)
        # fs.program_select(11, sfid, 0, 47)
        # fs.program_select(12, sfid, 0, 72)
        # fs.program_select(13, sfid, 0, 77)
        # fs.program_select(14, sfid, 0, 90)
        # fs.program_select(15, sfid, 0, 7)
        #
        # fs.program_select(16, sfid, 0, 50)
        # fs.program_select(17, sfid, 0, 11)
        # fs.program_select(18, sfid, 0, 16)
        # fs.program_select(19, sfid, 0, 26)
        # fs.program_select(20, sfid, 0, 70)
        # fs.program_select(21, sfid, 0, 63)
        # fs.program_select(22, sfid, 0, 75)
        # fs.program_select(23, sfid, 0, 1)
        #
        # fs.program_select(24, sfid, 0, 8)
        # fs.program_select(25, sfid, 0, 24)
        # fs.program_select(26, sfid, 0, 42)
        # fs.program_select(27, sfid, 0, 48)
        # fs.program_select(28, sfid, 0, 73)
        # fs.program_select(29, sfid, 0, 69)
        # fs.program_select(30, sfid, 0, 97)
        # fs.program_select(31, sfid, 0, 8)
        #
        #
        # fs.program_select(32, sfid, 0, 49)
        # fs.program_select(33, sfid, 0, 46)
        # fs.program_select(34, sfid, 0, 15)
        # fs.program_select(35, sfid, 0, 25)
        # fs.program_select(36, sfid, 0, 69)
        # fs.program_select(37, sfid, 0, 57) #62
        # fs.program_select(38, sfid, 0, 74)
        # fs.program_select(39, sfid, 0, 0)
        #
        # fs.program_select(40, sfid, 0, 7)
        # fs.program_select(41, sfid, 0, 43)
        # fs.program_select(42, sfid, 0, 41)
        # fs.program_select(43, sfid, 0, 47)
        # fs.program_select(44, sfid, 0, 72)
        # fs.program_select(45, sfid, 0, 77)
        # fs.program_select(46, sfid, 0, 90)
        # fs.program_select(47, sfid, 0, 7)
        #
        # fs.program_select(48, sfid, 0, 50)
        # fs.program_select(49, sfid, 0, 11)
        # fs.program_select(50, sfid, 0, 16)
        # fs.program_select(51, sfid, 0, 26)
        # fs.program_select(52, sfid, 0, 70)
        # fs.program_select(53, sfid, 0, 63)
        # fs.program_select(54, sfid, 0, 75)
        # fs.program_select(55, sfid, 0, 1)
        #
        # fs.program_select(56, sfid, 0, 8)
        # fs.program_select(57, sfid, 0, 24)
        # fs.program_select(58, sfid, 0, 42)
        # fs.program_select(59, sfid, 0, 48)
        # fs.program_select(60, sfid, 0, 73)
        # fs.program_select(61, sfid, 0, 69)
        # fs.program_select(62, sfid, 0, 97)
        # fs.program_select(63, sfid, 0, 8)

        #https://www.fluidsynth.org/api/group__reverb__effect.html
        #Original
        # roomsize=1.8
        # damping=0.001
        # width=1.8
        # level=5.8

        #Reverb setings preferred by Anirban
        #roomsize=1.8
        #damping=0.001
        #width=10.8
        #level=8.8

        #Original
        roomsize = 1.8
        damping = 0.001
        width = 5.8
        level = 7.5
        fs.set_reverb(roomsize, damping, width, level)
        logging.info("[Fluid Synth ] Fluid synth enabled")


def midi_instrument(instrument, bank=0, midi_chan=0):
    global fs, sfid
    fs.program_select(midi_chan, sfid, bank, instrument)


def midi_quit():
    """
    Function to close Midi channel on exit
    """
    global fs
    music = 0
    if fs is not None:
        fs.delete()
    del fs


def all_midi_off(counter=3):
    """
    Stop all midi notes
    """
    global midi_channels
    for chan in range(0, midi_channels-1):
        for note in range(0, 127):
            if (fs is not None):
                fs.noteoff(chan, note)
    counter -= 1
    if (counter > 0):
        Clock.schedule_once(lambda dt: all_midi_off(counter), 0.1)


def midi_on(prev_note=[C], notes_in=[C], vol=[MAX], panning=[50]):
    """
    Trigger an external midi note
    """
    global fs, instruments, midi_channels
    pan_ctrl = 10  # PAN_MSB
    bal_ctrl = 8
    note = list(dict.fromkeys(notes_in))  # remove duplicates
    i = 0
    for n in note:
        no = round(n)

        chan = no % midi_channels
        frac_note = round((no-n)*4096)
        #print("Vol:",vol[i])
        #volume = int(127-vol[i]*4)
        volume = int(vol[i])
        pan = panning[i]
        if(volume < 0):
            volume = 0
        for n1 in prev_note:
            if(no == round(n1)):
                #Flag as not to play again
                """ This prevents note retrigger if uncommented"""
                if(chan % 5 != 0):
                    n = 0  # Only continuous on some channels
                pass
        if(n > 0):
            #pan=chan*int(120/midi_channels)+7
            gm_instrument_num = instruments[chan]
            print("Note:", no, " Pitch:", frac_note, " Chan:", chan, " Pan:", pan, "Vol:",
                  volume, " GM_MIDI:", gm_instrument_num, "=", instrument_list[gm_instrument_num])
            # 74 is middle C, 127 is "how loud" - max is 127
            if (fs is not None):
                fs.noteon(chan, no, volume)
                fs.pitch_bend(chan, frac_note)
                fs.cc(chan, pan_ctrl, pan)
                fs.cc(chan, bal_ctrl, pan)
        i += 1


def midi_off(note=[C], note2=[C], volume=MAX):
    """
    Disable an external midi note
    """
    if (note != None):
        for n in note:
            no = round(n)
            chan = no % midi_channels
            #Check for notes that should not be off
            for n1 in note2:
                if(no == round(n1)):
                    #Flag as not to clear
                    n = 0
            if(n > 0):
                if (fs is not None):
                    fs.noteoff(chan, no)
