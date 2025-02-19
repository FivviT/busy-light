from config import Config
from server import Server

config = Config()
server = Server(config)
server.serve()
