"""
-------------------------------------------------
PyRealms Server
Copyright 2018 Peter Morgan
-------------------------------------------------
"""
from utils import log
from miniboa import TelnetServer
import globals as GLOBAL


def connect_hook(client):
    log.info("--> Received connection from {}, sending welcome banner".format(client.addrport()))
    # Get terminal environment
    client.request_naws()
    client.request_terminal_type()
    #client.request_mccp()
    #client.request_msp()
    client.send(GLOBAL.WELCOME_BANNER)
    #user = LoginHandler(client)
    GLOBAL.CLIENTS.append(client)
    #LOBBY[client] = user


def disconnect_hook(client):
    log.info("--> Lost connection to {}".format(client.addrport()))
    if client in GLOBAL.LOBBY.items():
        log.info('Removing {} from LOBBY'.format(client.addrport()))
        del GLOBAL.LOBBY[client]
        GLOBAL.CLIENTS.remove(client)


def kick_idlers():
    for c in GLOBAL.CLIENTS:
        if c.idle() > GLOBAL.IDLE_TIMEOUT:
            c.active = False
            log.info("Kicking idle client: {}".format(c.addrport()))


def process_commands():
    for c in GLOBAL.CLIENTS:
        if c in GLOBAL.LOBBY:
            GLOBAL.LOBBY[c].driver()
        elif c in GLOBAL.PLAYERS:
            GLOBAL.PLAYERS[c].driver()
"""
    for user in GLOBAL.LOBBY.values():
        # process commands
        pass
    for user in GLOBAL.PLAYERS.values():
        # process commands
        pass
"""


def main():

    log.info("Starting server on port {}".format(GLOBAL.PORT))

    server = TelnetServer(port=GLOBAL.PORT, timeout=.05)
    # set our own hooks for welcome/disconnect messaging
    server.on_connect = connect_hook
    server.on_disconnect = disconnect_hook

    while GLOBAL.GAME_RUNNING:
        # Tick / run game here
        server.poll()
        kick_idlers()
        process_commands()


    log.info("Server shutdown received")

if __name__ == '__main__':
    main()
