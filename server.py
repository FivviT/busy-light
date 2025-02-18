import sys
from time import sleep

import esp32

import led_control


def webpage(temperature, state, color):
    with open("/web/index.html", "r") as file:
        html = file.read()
    html = html.replace("{temperature}", str(temperature))
    html = html.replace("{color}", color)
    html = html.replace("{state}", "checked" if state == "ON" else "")
    return html


def serve(connection):
    # Start a web server
    state = "OFF"
    color = "#FFFFFF"
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            path = request.split()[1]
        except IndexError:
            pass
        if path == "/lighton?":
            led_control.set_color(color)
            state = "ON"
        elif path == "/lightoff?":
            led_control.turn_off()
            state = "OFF"
        elif path == "/change_color":
            color = ("#" + request.split("color=%23")[1].split(" ")[0])[:-1]
            if state == "ON":
                led_control.set_color(color)
        elif request == "/close?":
            sys.exit()
        temperature = esp32.mcu_temperature()
        html = webpage(temperature, state, color)
        client.send(html)
        client.close()
