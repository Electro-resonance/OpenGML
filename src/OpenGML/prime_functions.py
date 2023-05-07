# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 7th May 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Helper functions related to prime numbers
# =============================================================================


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