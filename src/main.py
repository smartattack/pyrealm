"""
-------------------------------------------------
PyRealms Server
Copyright 2018 Peter Morgan
-------------------------------------------------
"""
from utils import log
from miniboa import TelnetServer
import globals as GLOBAL
from user.login import Login
from user.db import boot_db

def connect_hook(client):
    log.info("--> Received connection from {}, sending welcome banner".format(client.addrport()))
    # Get terminal environment
    client.request_naws()
    client.request_terminal_type()
    #client.request_mccp()
    #client.request_msp()
    client.send(GLOBAL.WELCOME_BANNER)
    GLOBAL.CLIENTS.append(client)
    # Initial "user" is a login handler
    anonymous_user = Login(client)
    # Adding user to LOBBY activates it's driver() in main loop
    GLOBAL.LOBBY[client] = anonymous_user


def disconnect_hook(client):
    log.info("DISCONNECT_HOOK: Lost connection to {}".format(client.addrport()))
    if client in GLOBAL.LOBBY:
        log.info(' +-> Removing {} from LOBBY'.format(client.addrport()))
        del GLOBAL.LOBBY[client]
    if client in GLOBAL.PLAYERS:
        log.debug(' +-> Removing CLIENTS[{}]'.format(GLOBAL.PLAYERS[client].player.get_name()))
        del GLOBAL.PLAYERS[client]
    log.debug(' +-> Removing GLOBAL.CLIENTS[{}]'.format(client.addrport()))
    GLOBAL.CLIENTS.remove(client)



def kick_idlers():
    for c in GLOBAL.CLIENTS:
        if c.idle() > GLOBAL.IDLE_TIMEOUT:
            c.active = False
            log.info("Marking idle client inactive: {}".format(c.addrport()))


def process_commands():
    for user in list(GLOBAL.LOBBY.values()):
        # process commands
        if user._client.active and user._client.cmd_ready:
            user.driver()
    for user in GLOBAL.PLAYERS.values():
        # process commands
        if user._client.active and user._client.cmd_ready:
            user.driver()


def main():

    boot_db()
    
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
