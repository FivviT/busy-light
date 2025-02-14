import random
import time

import neopixel
from machine import Pin

pin = Pin(22)
n = neopixel.NeoPixel(pin, 12)

def random_color_blink():
    # Draw a red gradient.
    for i in range(12):
        n[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Update the strip.
    n.write()


    time.sleep(3)
    #turn off
    for i in range(12):
        n[i] = (0,0,0)

    n.write()