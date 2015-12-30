#! /usr/bin/env python

"""
Usage: logo.py logo.txt

Where logo.txt is text file with 40 character lines and 16 lines.
Space, 0x20, characters are black pixels
Non-space charaters are the "white" pixels
"""

import colorsys
import sys
import socket
import struct
import time

W = 40
H = 16

def C(h, l, s):
    """Convert hue, luminescence and saturation to an RGB string"""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return struct.pack("BBB", int(r * 255), int(g * 255), int(b * 255))


def L(text, f, b):
    """Convert text bitmap into 40x16 RGB bitmap with the given
    forground and background RGB strings"""
    d = ""
    lines = text.split("\n")
    i = 0
    for line in lines:
        j = 0
        for c in line:
            if c == ' ':
                d += b
            else:
                d += f
            j += 1
        d += b * (W - j)
        i += 1
    d += b * (H - i) * W
    return d

text = open(sys.argv[1]).read()

IP = socket.gethostbyname("matelight.rocks")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(600):
    d = L(text, C((i % 100)/100., 0.5, 1), C(0,0,0))
    s.sendto(d, (IP, 1337))
    time.sleep(0.05)
