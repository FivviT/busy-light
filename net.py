import socket

import network


def connect(ssid, password):
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")

    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")

    return ip


def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def get_connection(ssid, password):
	ip = connect(ssid, password)
	return open_socket(ip)
