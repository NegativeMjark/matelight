
#! /usr/bin/env python

"""
Usage: dots.py

Display randomly coloured, falling dots at random positions on the matelight.
Each dot falls at a different speed.
A new dot is added for every frame.
"""

import socket
import sys
import time
import colorsys
import struct
import array
import collections
import random


W = 40
H = 16

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

IP = socket.gethostbyname("matelight.rocks")

B = None

def clear(h, l, s):
    """Fill the buffer with pixels with the given hue, luminesence, and
    saturation"""
    global B
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    c = struct.pack("BBB", int(r * 255), int(g * 255), int(b * 255))
    B = array.array("B", c * W * H)

def set(x, y, h, l, s):
    """Set the pixel at the given location to the given hue, luminescence and
    saturation"""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    B[((y * W + x) * 3) + 0] = int(r * 255)
    B[((y * W + x) * 3) + 1] = int(g * 255)
    B[((y * W + x) * 3) + 2] = int(b * 255)


"""Dots have:
    Horizontal position: x
    Start time: t
    Velocity: 1 / v
    Hue: h
"""
Dot = collections.namedtuple("DOT", "x t v h")

dots = []

for i in range(200):
    # Add a new dot
    dots.append(Dot(
        h=(i % 20)/float(20),
        t=i,
        v=random.randint(1,8),
        x=random.randint(0, W - 1)
    ))

    # Clear the buffer with black.
    clear(0, 0, 0)

    # For each dot still on the display draw the dot at its current position
    dots_2 = []
    for dot in dots:
        y = (i - dot.t) / dot.v
        if y < H:
            set(dot.x, y, dot.h, 0.5, 1)
            dots_2.append(dot)
    dots = dots_2

    s.sendto(B.tostring(), (IP, 1337))
    time.sleep(0.05)
