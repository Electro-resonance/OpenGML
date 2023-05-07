# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 7th May 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Creates bonds between GML Singularities
# A class allowing linkage between GML singularities
# A bond represents a connection or a relationship between two singularities.
# It essentially creates a line or a curve connecting two singularities in the
# GML geometry.
# When a bond is created between two singularities, it causes them to interact
# with each other in a way that affects their behavior. The exact nature of the
# interaction depends on the parameters that are set for the bond, such as its
# strength, distance, and phase offset.
# In a physical system, the equivalent of a bond could be a force or a field
# that acts between two particles or objects.
# In phase space, bonds in OpenGML can represent a coupling between singularities
# that affects the way they oscillate or move through space. By creating a bond
# between two singularities, their oscillations become synchronized or correlated
# in some way, allowing them to affect each other's movement or behavior. This
# can be thought of as a kind of "gravitational" or "electromagnetic" interaction
# between the singularities in the phase space.
# =============================================================================

from colour_functions import *
import numpy as np
import GML

class GML_Bond:
    """
    A class to represent a bond between two singularities in OpenGML.
    """
    def __init__(self, singularity1, singularity2, phase_offset=0.0, coupling=0.1, color=BLACK, thickness=1):
        self.singularity1 = singularity1
        self.singularity2 = singularity2
        self.phase_offset = phase_offset
        self.coupling = coupling
        self.color = color
        self.thickness = thickness

    def update(self, dt=0):
        phase1=self.singularity1.phase[0]
        phase2=self.singularity2.phase[0]
        while (phase1-phase2)<180 :
            phase1+=360
        # Calculate the phase difference between the two singularities
        phase_diff = phase1 - phase2 + self.phase_offset

        phase_diff -= 360
        coupled_phase=self.coupling * phase_diff
        #print("phase_diff=",phase_diff," coupled=",coupled_phase)

        # Calculate the force on each singularity due to the bond
        force1 = coupled_phase
        force2 = -coupled_phase

        #print("force1=",force1," force2=",force2)

        # Apply the force to each singularity
        self.singularity1.apply_force(force1, dt)
        self.singularity2.apply_force(force2, dt)