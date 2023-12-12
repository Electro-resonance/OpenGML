#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 11th December 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: 3D Projection of Phase Prime Metric (PPM)
#
# Example Usage of Ordered Factor Function
#
# This script demonstrates an example usage of the 'ordered_factors' function
# from the 'prime_functions' library within the OpenGML project. It iterates through
# a range of numbers and computes their ordered factors, displaying the count and
# the factor combinations.
#
# Ensure the paths to the OpenGML project and prime_functions are correctly specified
# based on your system configuration.
# =============================================================================

import math
import sys

sys.path.append("../../src/OpenGML")  # AddOpenGML path
sys.path.append("../../src/OpenGML/prime_functions")  # AddOpenGML path

from prime_functions import ordered_factors

# Example usage or ordered factor function from prime_functions library:

for n in range (1,108+1):
    ordered_factors_count,ordered_factors_combinations = ordered_factors(n)
    print(f"OF({n}) = {ordered_factors_count}, Factors: {ordered_factors_combinations}")

    # Check if each combination multiplies out to the original number n
    for factors_combination in ordered_factors_combinations:
        if math.prod(factors_combination) != n:
            print(f"Invalid combination: {factors_combination}")