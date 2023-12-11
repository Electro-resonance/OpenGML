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

def is_prime(number):
    """
    Checks if a number is prime.
    :param number: The number to be checked.
    :return: True if the number is prime, False otherwise.
    """
    if number <= 1:
        return False

    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def generate_pattern_of_primes(n):
    """
    Generate the pattern of primes (difference between each prime)
    :param n: Maximum prime to consider
    :return: list containing the pattern
    """
    primes = generate_primes(n)
    pattern = []
    for i in range(len(primes) - 1):
        pattern.append(primes[i + 1] - primes[i])
    return pattern

def factorize(num_list, dimensions=4):
    """
    Given a list of integers, create a list of prime factors
    :param num_list: Input list
    :param dimensions:
    :return: output list of factors
    """
    factors = []
    for num in num_list:
        candidate = num
        prime_factors = []
        for i in range(dimensions - 1, 0, -1):
            if i == 1:
                prime_factors.append(num)
            else:
                while num % i == 0:
                    prime_factors.append(i)
                    num = num // i
        factors.append([candidate, prime_factors])
    return factors

def prime_factorization(num):
    """
    For a given number return a list of the prime factors
    :param num_list: Input number
    :return: output list of factors
    """
    factors = []
    divisor = 2
    while divisor <= num:
        if num % divisor == 0:
            factors.append(divisor)
            num = num / divisor
        else:
            divisor += 1
    return factors
