import random
import time

import neopixel
from machine import Pin

LEDS = 12

pin = Pin(22)
n = neopixel.NeoPixel(pin, LEDS)


def turn_on():
    for i in range(LEDS):
        n[i] = (255, 255, 255)
    n.write()


def turn_off():
    for i in range(LEDS):
        n[i] = (0, 0, 0)
    n.write()


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def set_color(color):
    if isinstance(color, str):
        color = hex_to_rgb(color)
    for i in range(LEDS):
        n[i] = color
    n.write()
