"""
-------------------------------------------------
PyRealms Server
Copyright 2018 Peter Morgan
-------------------------------------------------
"""
from utils import log
from miniboa import TelnetServer


# Game state / config
GAME_RUNNING = True
PORT = 1234
WELCOME_BANNER = '''
Welcome to PyRealm!

'''


def connect_hook(client):
    log.info("--> Received connection from {}, sending welcome banner".format(client.addrport()))
    client.send(WELCOME_BANNER)

def disconnect_hook(client):
    log.info("--> Lost connection to {}".format(client.addrport()))

def main():

    log.info("Starting server on port {}".format(PORT))

    server = TelnetServer(port=PORT, timeout=.05)
    # set our own hooks for welcome/disconnect messaging
    server.on_connect = connect_hook
    server.on_disconnect = disconnect_hook

    while GAME_RUNNING:
        # Tick / run game here
        server.poll()

    log.info("Server shutdown received")

if __name__ == '__main__':
    main()
