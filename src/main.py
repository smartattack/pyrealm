"""
-------------------------------------------------
PyRealms Server
Copyright 2018 Peter Morgan
-------------------------------------------------
"""

import time
import sys
import signal
from user.login import Login
from user.db import boot_userdb
from command.cmds_system import do_quit
from miniboa import TelnetServer
from utils import log
from database.tables import boot_db
import globals as GLOBALS
from update import update_time

def signal_handler(signal, frame):
    """Make sure we close the db on shutdown"""
    log.info('SIGINT caught, shutting down...')
    #sync_db()
    sys.exit(0)


def connect_hook(client):
    """Initialization routine run when clients connect"""
    log.info("--> Received connection from %s, sending welcome banner", client.addrport())
    # Get terminal environment
    client.request_naws()
    client.request_terminal_type()
    #client.request_mccp()
    #client.request_msp()
    client.send_cc(GLOBALS.WELCOME_BANNER)
    GLOBALS.clients.append(client)
    # Initial "user" is a login handler
    anonymous_user = Login(client)
    # Adding user to lobby activates it's driver() in main loop
    GLOBALS.lobby[client] = anonymous_user


def disconnect_hook(client):
    """Overrides miniboa hook, gets called on client disconnection"""
    log.info("DISCONNECT_HOOK: Lost connection to %s", client.addrport())
    if client in GLOBALS.lobby:
        log.info(' +-> Removing %s from lobby', client.addrport())
        del GLOBALS.lobby[client]
    if client in GLOBALS.players:
        log.debug(' +-> Removing clients[%s]', GLOBALS.players[client].player.name)
        GLOBALS.players[client].player.save(logout=True)
        if client in GLOBALS.actors:
            GLOBALS.actors.remove(GLOBALS.players[client])
        del GLOBALS.players[client]
    log.debug(' +-> Removing GLOBALS.clients[%s]', client.addrport())
    GLOBALS.clients.remove(client)



def kick_idlers():
    """Scan for and deactivate clients which have surpassed idle timeout"""
    # We maintain separate timeouts for players vs lobby connections
    for client in GLOBALS.clients:
        if client in GLOBALS.players:
            if client.idle() > GLOBALS.PLAYER_TIMEOUT:
                do_quit(GLOBALS.players[client].player, [])
                client.active = False
                log.info("Marking idle client inactive: %s", client.addrport())
        elif client in GLOBALS.lobby:
            if client.idle() > GLOBALS.LOBBY_TIMEOUT:
                client.active = False
                log.info("Marking idle client inactive: %s", client.addrport())
        else:
            log.error('Found client not in LOBBY or PLAYERS lists: %s', client.addrport())


def process_commands():
    """Handle user input"""
    for user in list(GLOBALS.lobby.values()):
        # process commands
        if user.client.active and user.client.cmd_ready:
            user.driver()
    for user in GLOBALS.players.values():
        # process commands
        if user.client.active and user.client.cmd_ready:
            user.driver()


def send_prompts():
    """Send user prompts"""
    for user in GLOBALS.players.values():
        if user.client.send_pending:
            user.send_prompt()


def main():
    """Pyrealms main()"""

    signal.signal(signal.SIGINT, signal_handler)

    # Start the clock
    GLOBALS.EPOCH_S = int(time.strftime('%s', time.strptime(GLOBALS.GAME_EPOCH, '%Y/%m/%d %H:%M:%S')))
    log.info('Converted GAME_EPOCH: %s -> %s', GLOBALS.GAME_EPOCH, GLOBALS.EPOCH_S)
    log.info('Game time will be scaled by a factor of: %s', GLOBALS.TIME_FACTOR)
    GLOBALS.boot_time = int(time.time())

    boot_userdb()
    boot_db()

    log.info("Starting server on port %s", GLOBALS.PORT)

    server = TelnetServer(port=GLOBALS.PORT, timeout=.05)
    # set our own hooks for welcome/disconnect messaging
    server.on_connect = connect_hook
    server.on_disconnect = disconnect_hook

    while GLOBALS.GAME_RUNNING:
        # Tick / run game here
        server.poll()
        kick_idlers()
        process_commands()
        send_prompts()
        update_time()

    log.info("Server shutdown received")

if __name__ == '__main__':
    main()
