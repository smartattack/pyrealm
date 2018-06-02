"""
-------------------------------------------------
PyRealms Server
Copyright 2018 Peter Morgan
-------------------------------------------------
"""
from utils import log
from miniboa import TelnetServer


# Default Game state / config
CLIENTS = []
IDLE_TIMEOUT = 300
GAME_RUNNING = True
PORT = 1234
WELCOME_BANNER = '''
Welcome to PyRealm!

'''



def connect_hook(client):
    log.info("--> Received connection from {}, sending welcome banner".format(client.addrport()))
    client.request_naws()
    client.request_terminal_type()
    #client.request_mccp()
    #client.request_msp()
    client.send(WELCOME_BANNER)
    CLIENTS.append(client)


def disconnect_hook(client):
    log.info("--> Lost connection to {}".format(client.addrport()))
    CLIENTS.remove(client)


def kick_idlers():
    for c in CLIENTS:
        if c.idle() > IDLE_TIMEOUT:
            c.active = False
            log.info("Kicking idle client: {}".format(c.addrport()))

def process():
    pass


def main():

    log.info("Starting server on port {}".format(PORT))

    server = TelnetServer(port=PORT, timeout=.05)
    # set our own hooks for welcome/disconnect messaging
    server.on_connect = connect_hook
    server.on_disconnect = disconnect_hook

    while GAME_RUNNING:
        # Tick / run game here
        server.poll()
        kick_idlers()
        process()

        

    log.info("Server shutdown received")

if __name__ == '__main__':
    main()
