import socket
import sys

import esp32
import network

import led_control


class Server:
    def __init__(self, config):
        self.config = config
        self.connection = self._connect_to_wifi()
        self.led_on = False
        self.color = self.config.get("color")
        self.color = self.config.get("color")
        self.temperature = esp32.mcu_temperature()
        self.led_control = led_control.LEDControl(config.get("leds"), config.get("pin"))


    def _connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.config.get("ssid"), self.config.get("password"))
        while not wlan.isconnected():
            print("Waiting for connection...")

        ip = wlan.ifconfig()[0]
        address = (ip, 80)
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        print(f"Connected on {ip}")
        return connection

    def webpage(self):
        with open("/web/index.html", "r") as file:
            html = file.read()
            html = html.replace("{temperature}", str(esp32.mcu_temperature()))
            html = html.replace("{color}", self.color)
            html = html.replace("{state}", "checked" if self.led_on else "")
        return html


    def serve(self):
        while True:
            client = self.connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            try:
                path = request.split()[1]
            except IndexError:
                pass
            if path == "/lighton?":
                self.led_control.set_color(self.color)
                self.led_on = True
            elif path == "/lightoff?":
                self.led_control.turn_off()
                self.led_on = False
            elif path == "/change_color":
                self.color = ("#" + request.split("color=%23")[1].split(" ")[0])[:-1]
                self.config.set("color", self.color)
                if self.led_on:
                    self.led_control.set_color(self.color)
            elif request == "/close?":
                sys.exit()
            html = self.webpage()
            client.send(html)
            client.close()
