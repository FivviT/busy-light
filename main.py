from config import Config
from server import Server


def main():
    config = Config()
    server = Server(config)
    server.serve()

if __name__ == "__main__":
    main()
