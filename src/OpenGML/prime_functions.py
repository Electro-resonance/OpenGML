# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 7th May 2023
# PPM Added: 11th December 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Helper functions related to prime numbers and PPM
# =============================================================================
import math
from collections import defaultdict

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

# Set initial values for the cache
# to speed up retrieval of already integers already tested as primes
prime_cache = {}

def is_prime_cached(num):
    """
    Checks if a number is prime.
    Caches all test results
    :param number: The number to be checked.
    :return: True if the number is prime, False otherwise.
    """
    global prime_cache
    if num in prime_cache:
        return prime_cache[num]
    if num < 2:
        prime_cache[num] = False
    else:
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                prime_cache[num] = False
                break
        else:
            prime_cache[num] = True
    return prime_cache[num]


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

def nth_prime(n):
    """
    Calculate the nth prime number.
    """
    primes = [2]
    candidate = 3

    while len(primes) < n:
        is_prime = True
        sqrt_candidate = math.isqrt(candidate)

        for prime in primes:
            if prime > sqrt_candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(candidate)

        candidate += 2

    return primes[-1]

def common_factors_recursive(n, current_factors=[], result=[]):
    """
    Recursive function to find all combinations of common factors for a given number.
    :param n: The number to find common factors for.
    :param current_factors: Current chain of factors.
    :param result: List to store valid combinations.
    """
    max_n = n // 2 + 1
    for i in range(2, max_n):
        if n % i == 0:
            new_factors = current_factors + [i]
            common_factors_recursive(n // i, new_factors, result)

    # If there are no more divisors, add the current chain of factors to the result
    #if not (n // 2 > 1):
    result1 = tuple(current_factors + [n])
    if len(result1) > 1:
        result.append(result1) # Add the factors found to the results
        result.append(result1[::-1]) # Also add the reverse order form

# Set initial values for the cache
# to speed up retrieval of already integers already tested as primes
ordered_factor_cache = defaultdict(list)

def ordered_factors(n,provide_factor_combinations=True):
    """
    Find all combinations of ordered factors for a given number.

    :param n: The number to find common factors for.
    :return: List of valid combinations.
    """
    global ordered_factor_cache
    if not provide_factor_combinations and n in ordered_factor_cache:
        return ordered_factor_cache[n]
    result = []
    common_factors_recursive(n, result=result)
    result = list(set(result))
    if(provide_factor_combinations==True):
        # Full response with the complete list
        return len(result), result
    else:
        # Faster response provides just the number of ordered factors
        ordered_factor_count = len(result)
        # Cache the result
        ordered_factor_cache[n] = ordered_factor_count
        return ordered_factor_count

def restrict(value, minimum, maximum):
    """
    Restrict a value within a specified range.

    :param value: The value to be restricted.
    :param minimum: The minimum allowable value.
    :param maximum: The maximum allowable value.
    :return: The restricted value within the specified range.
    """
    return min(max(value, minimum), maximum)