# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 16th May 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: functions used for symmetry breaking
# (creating new phase singularities and removing others)
# =============================================================================

import random
from prime_functions import is_prime
import GML_Bond

def symmetry_breaking(root, limit, min_freq=0.01, max_freq=200):
    """
    Symmetry breaking
    """
    number_children = len(root.children1)
    if (number_children == 0 or is_prime(number_children) == False):
        # Check if symmetry breaking should be applied
        if random.random() > 0.999:
            if random.random() > 0.5:
                child_freq = root.freq[0] / 2
            else:
                child_freq = root.freq[0] * 2
            if (child_freq > max_freq):
                child_freq = max_freq
            elif (child_freq < min_freq):
                child_freq = min_freq
            child_phase = root.phase[0]
            node = root.add_singularity(child_phase, root.diameter, child_freq, root.colour)

            for bond in root.bonds:
                if bond.singularity1 == root:
                    node.add_bond(node, bond.singularity2)
                if bond.singularity2 == root:
                    node.add_bond(node, bond.singularity1)

        elif random.random() > 0.999:
            if (number_children > 0):
                root.remove_child(root.children1[0])
    elif random.random() > 0.9999:
        if (number_children > 0):
            root.remove_child(root.children1[0])

    limit -= 1
    if (limit > 0):
        for child_node in root.children1:
            if (child_node != None):
                symmetry_breaking2(child_node,limit)
    return root


def symmetry_breaking2(root, limit, min_freq=0.01, max_freq=200):
    """
    Symmetry breaking
    """
    number_children = len(root.children1)
    if (number_children == 0 or is_prime(number_children) == False):
        # Check if symmetry breaking should be applied
        if random.random() > 0.999:
            # Apply symmetry breaking by adding a new child node
            if random.random() > 0.5:
                child_freq = root.freq[0] / 2
            else:
                child_freq = root.freq[0] * 2
            if child_freq > max_freq:
                child_freq = max_freq
            elif child_freq < min_freq:
                child_freq = min_freq
            child_phase = root.phase[0]
            node = root.add_singularity(child_phase, root.diameter, child_freq, root.colour)

            for bond in root.bonds:
                if bond.singularity1 == root:
                    node.add_bond(node, bond.singularity2)
                if bond.singularity2 == root:
                    node.add_bond(node, bond.singularity1)

        elif random.random() > 0.999:
            # Apply symmetry breaking by removing a child node
            if number_children > 0:
                root.remove_child(root.children1[0])

    elif random.random() > 0.9999:
        # Apply symmetry breaking by duplicating a child node
        if number_children > 0:
            child_node = root.children1[0]
            new_node = root.add_singularity(child_node.phase[0], child_node.diameter, child_node.freq[0],
                                            child_node.colour)
            for bond in child_node.bonds:
                new_node.add_bond(new_node, bond.singularity1)
                new_node.add_bond(new_node, bond.singularity2)
            # Apply symmetry breaking by rotating the duplicated child node
            angle = random.random() * 360
            if isinstance(new_node, list):
                new_node[0].set_phase(angle)
            else:
                new_node.set_phase(angle)
    limit -= 1
    if (limit > 0):
        for child_node in root.children1:
            if (child_node != None):
                symmetry_breaking2(child_node,limit)
    return root