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

    def _webpage(self):
        with open("/web/index.html", "r") as file:
            html = file.read()
            html = html.replace("{temperature}", str(esp32.mcu_temperature()))
            html = html.replace("{color}", self.color)
            html = html.replace("{state}", "checked" if self.led_on else "")
            html = html.replace("{icon_state}", "on" if self.led_on else "off")
            html = html.replace("{ssid}", self.config.get("ssid"))
            html = html.replace("{password}", self.config.get("password"))
            html = html.replace("{leds}", str(self.config.get("leds")))
        return html

    def _extract_path(self, request):
        try:
            return request.split()[1]
        except IndexError:
            return None

    def _extract_query(self, request):
        try:
            return request.split("?")[1].split(" ")[0]
        except IndexError:
            return ""
        
    def _extract_body_field(self, request, field) -> str:
        try:
            return (request.split(field + "=")[1].split(" ")[0]).replace("'", "")
        except IndexError:
            return ""


    def serve(self):
        while True:
            client = self.connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            path = self._extract_path(request)
            if path == "/lighton?":
                self.led_control.set_color(self.color)
                self.led_on = True
            elif path == "/lightoff?":
                self.led_control.turn_off()
                self.led_on = False
            elif path == "/change_wifi":
                ssid = self._extract_body_field(request, "ssid")
                password = self._extract_body_field(request, "password")
                self.config.set("ssid", ssid)
                self.config.set("password", password)
            elif path == "./change_leds":
                leds = self._extract_body_field(request, "leds")
                self.config.set("leds", leds)
                self.led_control = led_control.LEDControl(int(leds), self.config.get("pin"))
            elif path == "/change_color":
                self.color = self._extract_body_field(request, "color").replace("%23", "#").replace("'", "")
                self.config.set("color", self.color)
                if self.led_on:
                    self.led_control.set_color(self.color)
            elif request == "/close?":
                sys.exit()
            html = self._webpage()
            client.send(html)
            client.close()
