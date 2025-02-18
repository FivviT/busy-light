import json

from net import get_connection
from server import serve

with open(".config.json") as f:
    config = json.load(f)

connection = get_connection(config["ssid"], config["password"])
serve(connection)
