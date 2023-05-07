# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 24th February 2022
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Sonification class for Geometric Music Language (GML)
# =============================================================================


from GML import *
from gl_text_drawing import *
from midi_functions import *


str_modes = ["Free Running", "Winfree Reset", "Microtubule", "Undefined"]
str_draw_modes = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]


volume_curve = [1., 1., 1., 1., 1., 1., 1., 1., 1.,
                1., 1., 1., 1., 1., 1., 1., 1., 1.,
                1., 1., 1., 1., 1., 1., 1., 1., 1.,
                1., 1., 1., 1., 1., 1., 1., 1., 1.,
                1., 1., 1., 1., 1., 1., 1., 1., 1.,
                1., 1., 1., 0.938, 0.861, 0.793, 0.731, 0.675, 0.624,
                0.577, 0.535, 0.496, 0.462, 0.432, 0.404, 0.379, 0.355, 0.334,
                0.315, 0.297, 0.281, 0.266, 0.253, 0.241, 0.231, 0.222, 0.214,
                0.206, 0.198, 0.191, 0.185, 0.179, 0.174, 0.17, 0.166, 0.164,
                0.162, 0.163, 0.166, 0.173, 0.184, 0.198, 0.213, 0.228, 0.239,
                0.245, 0.244, 0.234, 0.215, 0.193, 0.171, 0.153, 0.14, 0.13,
                0.122, 0.117, 0.113, 0.111, 0.111, 0.112, 0.114, 0.118, 0.125,
                0.134, 0.146, 0.162, 0.183, 0.211, 0.246, 0.29, 0.343, 0.406,
                0.475, 0.55, 0.625, 0.692, 0.742, 0.768, 0.762, 0.723, 0.651,
                0.555, 0.555, 0.555, 0.555]


def Sonic_GML_init():
    """
    Initialise Midi functions
    """
    midi_init()


def Sonic_GML_quit():
    """
    Function to close Midi channel on exit
    """
    midi_quit()


class Sonic_GML():
    """
    Class for sonification of a GML nested tree of oscillators
    """
    octaves = 10
    notes = []
    notes_volumes = []
    notes_panning = []
    notes_on = []
    notes_on_volumes = []
    notes_on_panning = []
    prev_notes = []
    note_num = 0
    note_pos = []
    orbit_pos = []
    notes_on_pos = []
    chord_size = 64
    note_loop = 0
    log_music_mode = True
    music_scale = 12.0
    gml_mode = 0
    draw_mode = 2
    star = None
    blue_dot = None
    green_dot = None
    green_dot_size = 7
    blue_dot_size = 5
    blip = None
    blip_vol = []
    phase_advance = 0.5
    pitch_offset = 12  # Default 12 semitone (one octave pitch offset)
    cursor_phase_overlap = 20  # Was 20 before video added
    average_note = 50
    average_note2 = 50

    def __init__(self):
        """
        Initialise the class
        """
        self.chord_size = 100
        for i in range(0, 255):
            self.blip_vol.append(None)
        self.graphics_helper = GML_graphics_helper()
        self.pos_mid = self.graphics_helper.screen_get_mid_position()

    def set_pitch_offset(self, pitch_offset):
        """
        Pitch offset in semitones
        12 = one octave (default)
        24 = two octaves
        36 = three octaves
        """
        self.pitch_offset = pitch_offset

    def increment_octaves(self, inc):
        """
        Increment (or decrement) the octave range
        """
        self.octaves += inc
        if(self.octaves < 1):
            self.octaves = 1
        elif(self.octaves > 10):
            self.octaves = 10

    def increment_chord_size(self, inc):
        """
        Increment (or decrement) the number of notes in a chord
        """
        self.chord_size += inc
        if(self.chord_size < 1):
            self.chord_size = 1
        elif(self.chord_size > 128):
            self.chord_size = 128

    def set_log_music(self, log_music):
        """
        Select linear or logarithmic note mapping
        """
        self.log_music_mode = log_music

    def set_music_scale(self, music_scale):
        """
        Multiplier for log modes
        """
        self.music_scale = music_scale

    def increment_gml_mode(self, inc):
        """
        Increment (or decrement) the GML mode
        """
        self.gml_mode += inc
        if(self.gml_mode < 0):
            self.gml_mode = 3
        elif(self.gml_mode > 3):
            self.gml_mode = 0

    def increment_draw_mode(self, inc, rootGML):
        """
        Increment (or decrement) the draw mode
        """
        self.draw_mode += inc
        if(self.draw_mode < 0):
            self.draw_mode = 8
        elif(self.draw_mode > 8):
            self.draw_mode = 0
        if(rootGML != None):
            rootGML.set_draw_mode(self.draw_mode)

    def all_midi_notes_off(self):
        all_midi_off()

    def build_note_seq_nested(self, parent_node):
        """
        Build a sequence of notes from the GML nested tree
        using distance to determine pitch of the note
        """
        if(parent_node.oscillators() > 10000):
            return
        note=parent_node.distanceTo(self.pos_mid)/10
        if(note>40):
            note=40
        if (note < 20):
            note =20
        self.notes.append(note)
        [px, py] = parent_node.get_cartesian_pos()
        self.note_pos.append([px, py, 5])
        self.note_num += 1
        self.notes_volumes.append(100)
        self.notes_panning.append(50)
        if (parent_node.children1 != None):
            for child in parent_node.children1:
                self.build_note_seq_nested(child)
        return

    def build_rhythms_nested(self, parent_node):
        """
        Convert the GML nested tree into groups of pitches based
        on proximity of a set of cursors to the singularity points
        """
        parent_node.cursor_phase[0]= + 90

        if(self.gml_mode != 2 or parent_node.get_relay_flag() == True):
            parent_node.advance_cursor(self.phase_advance)
        parent_node.calc_cursor_pos()
        if(parent_node.oscillators() > 10000):
            return
        [px, py] = parent_node.return_cursor_pos()
        diff = parent_node.cursor_overlap_check(self.cursor_phase_overlap)
        vol = (127*(32-diff[1])/32)  # Convert bing to volume change

        if(diff[0] == True):
            if (parent_node.parent != None):
                new_note = 3000 / parent_node.cursor_radius()
                if(self.log_music_mode == True):
                    new_note = math.log(new_note) / \
                                        math.log(2.0)*self.music_scale
                new_note += self.pitch_offset
                #if(self.note_num<4):
                self.notes.append(new_note)
                prob_volume = vol*parent_node.probability_volume()
                if(prob_volume) < 10:
                    prob_volume = 10
                elif (prob_volume > 127):
                    prob_volume = 127
                #print("Vol:",vol," prob_volume",prob_volume,"prob",parent_node.probability_volume())
                self.notes_volumes.append(prob_volume)
                pan = int(parent_node.mypos[0]/5.05)-49  # *640/127 x width
                #print("Pan:",pan)
                self.notes_panning.append(pan)
                self.note_pos.append([px, py, diff[1]])
                self.note_num += 1
        else:
            self.orbit_pos.append([px, py, parent_node.relay_flag])
        if (parent_node.children1 != None):
            for child in parent_node.children1:
                child.cursor_phase[0] = parent_node.cursor_phase[0]
                self.build_rhythms_nested(child)
        return

    def build_all_notes_nested(self, parent_node):
        """
        Convert the GML nested tree into groups of pitches based
        on proximity of a set of cursors to the singularity points
        """
        if(self.gml_mode != 2 or parent_node.get_relay_flag() == True):
            parent_node.advance_cursor(self.phase_advance)
        parent_node.calc_cursor_pos()
        if(parent_node.oscillators() > 10000):
            return
        [px, py] = parent_node.return_cursor_pos()
        diff = parent_node.cursor_overlap_check(self.cursor_phase_overlap)

        vol = (127*(32-diff[1])/32)  # Convert bing to volume change
        #if (self.gml_mode == 2 and parent_node.parent == None):
        #     parent_node.set_relay_flag(True)
        #     for child_node in parent_node.children1:
        #         child_node.set_relay_flag(True)
        #     print("Relay Switch1")

        if(diff[0] == True):
            if (self.gml_mode == 2):
                parent_node.set_relay_flag(False)
                for child_node in parent_node.children1:
                    child_node.set_relay_flag(True)
                #print("Relay Switch2")
            #Pass relay_flag back
            if (self.gml_mode == 2 and parent_node.parent != None):
                if(parent_node.get_relay_flag() == True):
                    parent_node.set_relay_flag(False)
                    parent_node.parent.set_relay_flag(True)
                    #print("Relay Switch3")
                elif(parent_node.parent.get_relay_flag() == True):
                    parent_node.set_relay_flag(True)
                    parent_node.parent.set_relay_flag(False)
                    #print("Relay Switch4")
            #Check for gml clock reset mode
            if(parent_node.parent != None and self.gml_mode == 1 and diff[1] < 1):
                parent_node.reset_child_cursors(99)
                print("Resetting child cursors")
            if (parent_node.parent != None):
                new_note = 400/parent_node.cursor_radius()
                if(self.log_music_mode == True):
                    new_note = math.log(new_note) / \
                                        math.log(2.0)*self.music_scale
                new_note += self.pitch_offset
                #if(self.note_num<4):
                self.notes.append(new_note)
                prob_volume = vol*parent_node.probability_volume()
                if(prob_volume) < 10:
                    prob_volume = 10
                elif (prob_volume > 127):
                    prob_volume = 127
                #print("Vol:",vol," prob_volume",prob_volume,"prob",parent_node.probability_volume())
                self.notes_volumes.append(prob_volume)
                pan = int(parent_node.mypos[0]/5.05)-49  # *640/127 x width
                #print("Pan:",pan)
                self.notes_panning.append(pan)
                self.note_pos.append([px, py, diff[1]])
                self.note_num += 1
        else:
            self.orbit_pos.append([px, py, parent_node.relay_flag])
        if (parent_node.children1 != None):
            for child in parent_node.children1:
                self.build_all_notes_nested(child)
        return

    def circle_notes(self):
        """
        Draw circles around the singularity points for
        which sound is being made
        """
        if(self.draw_mode >= 6 and GMLBaseClass.draw_mode < 7):
            for pos in self.orbit_pos:
                #Show a blue dot for the cursor
                pos1 = [pos[0], pos[1]]
                if (pos[2] == True):
                    if(self.green_dot == None):
                        self.green_dot = self.graphics_helper.create_circular_blit(pos1, self.green_dot_size, 0, [
                                                              70, 255, 70], [0, 0, 0], 100, False, 0)
                    else:
                        self.graphics_helper.plot_centre_blit(self.green_dot, pos1)
                else:
                    if(self.blue_dot == None):
                        self.blue_dot = self.graphics_helper.create_circular_blit(pos1, self.blue_dot_size, 0, [
                                                             70, 70, 255], [0, 0, 0], 100, False, 0)
                    else:
                        self.graphics_helper.plot_centre_blit(self.blue_dot, pos1)
        for [p1, p2, v] in self.notes_on_pos:
            bing_vol = int(255-v*5)
            if(bing_vol < 0):
                bing_vol = 0
            r = int((10-v)/1.5)  # radius of bing dot
            if(r < self.blue_dot_size):
                r = self.blue_dot_size
            pos = [p1, p2]
            if(self.draw_mode >= 1):
                if(self.blip_vol[bing_vol] == None):
                    self.blip_vol[bing_vol] = self.graphics_helper.create_circular_blit(
                        pos, r, 0, [240, 0, bing_vol], [0, 0, 0], 190, False, 0)
                else:
                    self.graphics_helper.plot_centre_blit(self.blip_vol[bing_vol], pos)
                if(self.blip == None):
                    self.blip = self.graphics_helper.create_circular_blit(
                        pos, 1, 0, [240, 240, 240], [0, 0, 0], 190, False, 0)
                else:
                    self.graphics_helper.plot_centre_blit(self.blip, pos)
            if(v < 12):
                if(self.draw_mode >= 1):
                    #Draw star
                    if(self.star == None):
                        self.star = self.graphics_helper.create_star_blit(
                            pos, r*3, 4, [255, 0, 0], [0, 0, 0], 190)
                    else:
                        self.graphics_helper.plot_centre_blit(self.star, pos)

    def constrain_notes(self, note, avg):
        while(note > avg):
            note -= 12
        while(note < avg-64):
            note += 12
        return note

    def constrain_notes_high_pitch(self, note, avg):
        while(note > avg+12):
            note -= 12
        while(note < avg-12):
            note += 12

        # if(note>85):
        #     n=note/2
        return note

    def adjust_volume_freq(self, volume, midi_note):
        global volume_curve
        #print(midi_note)
        if(midi_note < 128):
            new_vol = volume*volume_curve[int(midi_note)]
        else:
            new_vol = volume
        return new_vol

    def play_sonic_sequence(self, rootNode, sequence=False):
        """
        Build up a set of notes to play and also
        decide which notes to stop playing
        """
        self.note_num = 0
        self.orbit_pos.clear()
        if(sequence==True):
            #self.build_note_seq_nested(rootNode)
            self.build_rhythms_nested(rootNode)
        else:
            self.build_all_notes_nested(rootNode)
        self.notes_on_pos.clear()

        for i in range(0, self.chord_size):
           if(self.note_loop >= len(self.notes)):
               self.note_loop = 0
           if(len(self.notes) > 0):
               n = self.notes[self.note_loop]
               self.average_note = (n+2*self.average_note)/3
               self.average_note2 = (n+self.average_note2)/2
               v = self.notes_volumes[self.note_loop]
               p = self.notes_panning[self.note_loop]
               #pygame.draw.circle(screen,[240,0,240], note_pos[note_loop] , 10, 0)

               lowest_note = 76-((self.octaves/2+1)*12)
               highest_note = lowest_note+self.octaves*12

               while (n >= highest_note or n > 127):
                   n -= 12
               while (n < lowest_note or n < 0):
                   n += 12

               n = self.constrain_notes(n, self.average_note)
               v = self.adjust_volume_freq(v, n)
               self.notes_on.append(n)
               self.notes_on_volumes.append(v*0.7)
               self.notes_on_panning.append(p)
               self.notes_on_pos.append(self.note_pos[self.note_loop])

               sub_bass_note = n
               while(sub_bass_note > 18):
                   sub_bass_note -= 12
               if(sub_bass_note >= 0):
                   self.notes_on.append(sub_bass_note)
                   self.notes_on_volumes.append(v)
                   self.notes_on_panning.append(p+3)
                   self.notes_on_pos.append(self.note_pos[self.note_loop])

               n = self.constrain_notes_high_pitch(n, self.average_note2)
               v = self.adjust_volume_freq(v, n)
               self.notes_on.append(n)
               self.notes_on_volumes.append(v*0.2)
               self.notes_on_panning.append(p-3)
               self.notes_on_pos.append(self.note_pos[self.note_loop])

               self.note_loop += 1

        midi_off(self.prev_notes, self.notes_on)
        midi_on(self.prev_notes, self.notes_on,
                self.notes_on_volumes, self.notes_on_panning)
        #pygame.time.delay(200)
        self.prev_notes.clear()
        for note in self.notes_on:
            self.prev_notes.append(note)
        self.notes_on.clear()
        self.notes_on_volumes.clear()
        self.notes_on_panning.clear()
        self.notes.clear()
        self.notes_volumes.clear()
        self.notes_panning.clear()
        self.note_pos.clear()

    def drawText(self, text_draw, text_canvas, offset, x=10):
        """
        Draw text related to the options selected
        """
        text_draw.drawText(text_canvas, x, offset,
                           "Chord Size: " + str(int(self.chord_size)), 18)
        text_draw.drawText(text_canvas, x, offset+20,
                           "Octaves: " + str(int(self.octaves)), 18)
        if(self.log_music_mode == True):
            text_draw.drawText(text_canvas, x, offset+40, "Music: log", 18)
        else:
            text_draw.drawText(text_canvas, x, offset+40, "Music: lin", 18)
        text_draw.drawText(text_canvas, x, offset+60,
                           "Scale: " + str(int(self.music_scale*10)/10), 18)
        text_draw.drawText(text_canvas, x, offset+80,
                           "GML: " + str_modes[self.gml_mode], 18)
        text_draw.drawText(text_canvas, x, offset+100,
                           "Detail: " + str_draw_modes[self.draw_mode], 18)
