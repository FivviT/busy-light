import neopixel
from machine import Pin


class LEDControl:
    def __init__(self, leds=12, pin=22):
        self.leds_count = leds
        self.pin = Pin(pin)
        self.n = neopixel.NeoPixel(self.pin, self.leds_count)


    def turn_off(self):
        #set all leds to black
        for i in range(self.leds_count):
            self.n[i] = (0, 0, 0)
        self.n.write()

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def set_color(self, color):
        if isinstance(color, str):
            color = self._hex_to_rgb(color)
        for i in range(self.leds_count):
            self.n[i] = color
        self.n.write()

