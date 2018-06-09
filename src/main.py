"""
-------------------------------------------------
PyRealms Server
Copyright 2018 Peter Morgan
-------------------------------------------------
"""
from utils import log
from miniboa import TelnetServer
import globals as GLOBALS
from user.login import Login
from actor.player import Player
from user.db import boot_db

def connect_hook(client):
    log.info("--> Received connection from {}, sending welcome banner".format(client.addrport()))
    # Get terminal environment
    client.request_naws()
    client.request_terminal_type()
    #client.request_mccp()
    #client.request_msp()
    client.send(GLOBALS.WELCOME_BANNER)
    GLOBALS.CLIENTS.append(client)
    # Initial "user" is a login handler
    anonymous_user = Login(client)
    # Adding user to LOBBY activates it's driver() in main loop
    GLOBALS.LOBBY[client] = anonymous_user


def disconnect_hook(client):
    log.info("DISCONNECT_HOOK: Lost connection to {}".format(client.addrport()))
    if client in GLOBALS.LOBBY:
        log.info(' +-> Removing {} from LOBBY'.format(client.addrport()))
        del GLOBALS.LOBBY[client]
    if client in GLOBALS.PLAYERS:
        log.debug(' +-> Removing CLIENTS[{}]'.format(GLOBALS.PLAYERS[client].player.get_name()))
        GLOBALS.PLAYERS[client].player.save(logout = True)
        del GLOBALS.PLAYERS[client]
    log.debug(' +-> Removing GLOBALS.CLIENTS[{}]'.format(client.addrport()))
    GLOBALS.CLIENTS.remove(client)



def kick_idlers():
    for c in GLOBALS.CLIENTS:
        if c.idle() > GLOBALS.IDLE_TIMEOUT:
            c.active = False
            log.info("Marking idle client inactive: {}".format(c.addrport()))


def process_commands():
    for user in list(GLOBALS.LOBBY.values()):
        # process commands
        if user._client.active and user._client.cmd_ready:
            user.driver()
    for user in GLOBALS.PLAYERS.values():
        # process commands
        if user._client.active and user._client.cmd_ready:
            user.driver()


def main():

    boot_db()
    
    log.info("Starting server on port {}".format(GLOBALS.PORT))

    server = TelnetServer(port=GLOBALS.PORT, timeout=.05)
    # set our own hooks for welcome/disconnect messaging
    server.on_connect = connect_hook
    server.on_disconnect = disconnect_hook

    while GLOBALS.GAME_RUNNING:
        # Tick / run game here
        server.poll()
        kick_idlers()
        process_commands()


    log.info("Server shutdown received")

if __name__ == '__main__':
    main()
