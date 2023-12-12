#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 11th December 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: 3D Projection of Phase Prime Metric (PPM)

# This script generates a 3D visualization of the Phase Prime Metric (PPM).
# The PPM is a mathematical concept that combines prime numbers, ordered factors,
# and a number's position on the integer number line. It provides insights into the
# relationships between these elements in a 3D space.

# Controls:
#   - Arrow keys: Rotate the 3D plot to view different perspectives.
#   - 'Q' key: Increment PPM factorisation value.
#   - 'A' key: Decrement PPM factorisation value.
#   - 'W' key: Increment PPM size.
#   - 'S' key: Decrement PPM size.
#   - 'P' key: Pause/unpause rotation.
#   - 'F' key: Toggle full-screen mode.
#   - 'U' key: Toggle auto-centering mode.

# To use this script, ensure you have the required libraries installed:
#   - Pygame: pip install pygame
#   - PyOpenGL: pip install PyOpenGL
# Run the script and use the mentioned keys to interact with the 3D plot.

# For more information and updates, visit the OpenGML project on GitHub.
# =============================================================================

import sys

sys.path.append("../../src/OpenGML")  # AddOpenGML path
sys.path.append("../../src/OpenGML/prime_functions")  # AddOpenGML path

from prime_functions import is_prime_cached
from prime_functions import ordered_factors
from prime_functions import restrict

import pygame
from pygame.locals import *
import math


# Dictionary to store prime angles for the polar plot
prime_angle_table = {}

def allocate_angles(max_prime):
    """
    Allocate angles to primes for the polar plot.

    :param max_prime: The maximum prime number to consider.
    :return: Dictionary with prime numbers as keys and their allocated angles as values.
    """
    global prime_angle_table
    angle_step = 24  # degrees
    current_angle = 0

    # Iterate through numbers up to the maximum prime
    for n in range(2, max_prime):
        # Check if the number is prime
        if is_prime_cached(n):
            prime_angle_table[n] = current_angle
            current_angle += angle_step

    # Return the prime angle table
    return prime_angle_table


def generate_ordered_factors_plot(order=0, num_points=500):
    """
    Generate data points for the ordered factors plot.

    :param order: The order value for filtering points. If 0, all points are considered.
    :param num_points: The number of points to generate.
    :return: List of tuples representing (x, y, z, theta, radius) for each point.
    """
    x_values = []
    y_values = []
    z_values = []
    theta_values = []
    radius_values = []

    for n in range(1, num_points):
        # Filter points based on the order value
        if order > 1 and n % order != 0:
            continue

        # Calculate the ordered factors count
        ordered_factors_count = ordered_factors(n, provide_factor_combinations=False)

        # Iterate through prime factors
        for factor in prime_angle_table:
            # Check if the point is associated with the current prime factor
            if n % factor == 0:
                # Rotate the point around the prime factor
                for rotate in range(0, 24):
                    theta_base = prime_angle_table[factor]
                    theta = (theta_base + rotate * 15)  # * 2 * math.pi
                    radius = ordered_factors_count
                    x = radius * math.sin(theta)
                    y = radius * math.cos(theta)
                    x_values.append(x)
                    y_values.append(y)
                    z_values.append(n)
                    theta_values.append(theta_base)
                    radius_values.append(radius)

    # Return the generated data points
    return list(zip(x_values, y_values, z_values, theta_values, radius_values))


def calculate_shading(normal, light_direction):
    """
    Calculate shading intensity based on the dot product of the normal vector and light direction.

    :param normal: The normal vector of the surface.
    :param light_direction: The direction vector of the light source.
    :return: Shading intensity value between 0 and 1.
    """
    # Ensure the dot product is in the valid range [0, 1]
    dot_product = max(0, sum(a * b for a, b in zip(normal, light_direction)))
    return dot_product


def display_text(order, num_points, angle_x, angle_y):
    """
    Display text information on the screen.

    :param order: The order value to be displayed.
    :param num_points: The number of points to be displayed.
    :param angle_x: The X-axis rotation angle to be displayed.
    :param angle_y: The Y-axis rotation angle to be displayed.
    """
    # Round the rotation angles for better readability
    angle_x=round(angle_x/math.pi*180,1)
    angle_y = round(angle_y / math.pi * 180, 1)

    # Render text surfaces
    order_text = font.render(f"Order: {order}", True, (255, 255, 255))
    points_text = font.render(f"Number of Points: {num_points}", True, (255, 255, 255))
    x_text = font.render(f"X: {angle_x}", True, (255, 255, 255))
    y_text = font.render(f"Y: {angle_y}", True, (255, 255, 255))

    # Blit the text surfaces onto the screen
    screen.blit(order_text, (10, 10))
    screen.blit(points_text, (10, 50))
    screen.blit(x_text, (10, 90))
    screen.blit(y_text, (10, 130))



# Initialize Pygame Display Engine
pygame.init()

fullscreen = False
# Set up display
width, height = 1747, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ordered Factors 3D Plot")

# Set up clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.Font(None, 36)

plot_points=None

# Set initial camera position
camera_distance = 500
angle_x = -math.pi/2 - math.pi/30
angle_y = - math.pi/10

# Flags to track key state
key_up = False
key_down = False
key_left = False
key_right = False
inc_order= False
dec_order= False
inc_points= False
dec_points= False
autoscale_autocenter = True

pause=True
order=1
frac_order=1

# Calculate the center of the plot
center_x = 1000
center_y = 500

# Calculate the width and height of the plot
plot_width = 2024
plot_height = 1024

new_scale=1

num_points=1000
acceleration=5

# Populate primes for use in the polar plot
allocate_angles(37)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                key_up = True
            elif event.key == K_DOWN:
                key_down = True
            elif event.key == K_LEFT:
                key_left = True
            elif event.key == K_RIGHT:
                key_right = True
            elif event.key == K_p:
                pause = not pause
            elif event.key == K_q:
                inc_order=True
            elif event.key == K_a:
                dec_order=True
            elif event.key == K_w:
                inc_points=True
            elif event.key == K_s:
                dec_points=True
            elif event.type == KEYDOWN and event.key == K_f:
                # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width, height))
            elif event.key == K_u:
                autoscale_autocenter = not autoscale_autocenter
        elif event.type == KEYUP:
            if event.key == K_UP:
                key_up = False
            elif event.key == K_DOWN:
                key_down = False
            elif event.key == K_LEFT:
                key_left = False
            elif event.key == K_RIGHT:
                key_right = False
            elif event.key == K_q:
                inc_order=False
            elif event.key == K_a:
                dec_order=False
            elif event.key == K_w:
                inc_points=False
            elif event.key == K_s:
                dec_points=False

    # Update angles based on key state
    if key_up:
        angle_x += 0.1
    elif key_down:
        angle_x -= 0.1
    if key_left:
        angle_y += 0.1
    elif key_right:
        angle_y -= 0.1

    if (inc_order==True and frac_order<num_points):
        frac_order+=0.5
        order = int(frac_order)
        plot_points=None #Trigger recalc
    if (dec_order==True and frac_order>1):
        frac_order-=0.5
        order = int(frac_order)
        plot_points=None #Trigger recalc
    if (inc_points==True and num_points<4000):
        num_points+=1
        plot_points=None #Trigger recalc
    if (dec_points==True and num_points>1):
        num_points-=1
        plot_points=None #Trigger recalc

    #Keep moving
    if(pause==False):
        angle_x += 0.004
        angle_y += 0.004

    # Redraw
    screen.fill((0,0,0)) #Black background

    if plot_points is None:
        #Recalculate for changes
        plot_points = generate_ordered_factors_plot(order,num_points)

    # A point index counter used for shading
    point_index=0

    last_x=0
    last_y=0

    minx = miny = float('inf')
    maxx = maxy = float('-inf')

    for point in plot_points:
        point_index=point_index+1
        rotated_x = point[0] * math.cos(angle_y) - point[2] * 2 * math.sin(angle_y)
        rotated_z = point[0] * math.sin(angle_y) + point[2] * 2 * math.cos(angle_y)
        rotated_y = point[1] * math.cos(angle_x) - rotated_z * math.sin(angle_x)

        #scale = 1
        rotated_x = rotated_x * new_scale
        rotated_y = rotated_y * new_scale
        #rotated_z = rotated_z / scale

        scaled_x = int((rotated_x + width-center_x) / 2)
        scaled_y = int((rotated_y + height-center_y+500) / 2)
        scaled_z = int((rotated_z + height) / 2)

        minx = min(minx, rotated_x)
        maxx = max(maxx, rotated_x)
        miny = min(miny, rotated_y)
        maxy = max(maxy, rotated_y)


        # Calculate shading based on the normal vector (assuming light is coming from the positive z direction)
        #normal = [rotated_x, rotated_y, point[2]]
        #light_direction = [0, 0, 1]
        #shading = calculate_shading(normal, light_direction)
        # Use shading to set color
        #shade=shading+100
        #r=g=b=int(shade)
        #r = restrict(r, 0, 255)

        b = point_index/100
        g = point[3] #theta

        # Restrict color values to the valid range (0 to 255)
        b = restrict(b, 0, 255)
        g = restrict(g, 0, 255)

        # Draw small and large circles for each point on the screen
        pygame.draw.circle(screen, (255, g, b), (scaled_x, scaled_y - 300), 1, 1)  # Small circle
        pygame.draw.circle(screen, (0, g, b), (scaled_x, scaled_y - 300), 3, 1)  # Large circle

        # Check if there is a last position to draw a line from
        if last_x != 0 and last_y != 0:
            # Calculate color values based on the radius of the point
            r = point[4] % 10 * 10 + 50  # Red component based on the radius
            g = point[4] / 5  # Green component based on the radius
            b = point[4] % 13 * 10 + 50  # Blue component based on the radius

            # Restrict color values to the valid range (0 to 255)
            r = restrict(r, 0, 255)
            g = restrict(g, 0, 255)
            b = restrict(b, 0, 255)

            # Draw a line connecting the current point to the last point
            pygame.draw.line(screen, (r, g, b), (last_x, last_y - 300), (scaled_x, scaled_y - 300), 1)

        # Store latest point
        last_x=scaled_x
        last_y=scaled_y

    # Calculate the center of the plot
    center_x = ((center_x  * acceleration) + ((minx + maxx) / 2))/(acceleration+1)
    center_y = ((center_y  * acceleration) + ((miny + maxy) / 2))/(acceleration+1)

    # Calculate the width and height of the plot
    plot_width = maxx - minx
    plot_height = maxy - miny

    # Calculate the new scale based on the smaller dimension
    new_scale = (new_scale * acceleration + min(width / plot_width, height / plot_height))/(acceleration+1)

    # Display the text info
    display_text(order,num_points,angle_x,angle_y)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(20)

# Close pygame engine
pygame.quit()