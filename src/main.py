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
from database.tables import boot_db, sync_db, save_object
from update import update_game_time
from event import EventQueue
import globals as GLOBALS


# Debugging
from debug import update_snapshot, log_objgraph

def signal_handler(signal, frame):
    """Make sure we close the db on shutdown"""
    log.info('SIGINT caught, shutting down...')
    sync_db(force=True)
    sys.exit(0)


def connect_hook(client):
    """Initialization routine run when clients connect"""
    log.info('--> Received connection from %s, sending welcome banner', client.addrport())
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
        save_object(GLOBALS.players[client].player, logout=True)
        # FIXME: clean up player from instances/structures
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
                log.info('Marking idle client inactive: %s', client.addrport())
        elif client in GLOBALS.lobby:
            if client.idle() > GLOBALS.LOBBY_TIMEOUT:
                client.active = False
                log.info('Marking idle client inactive: %s', client.addrport())
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
    GLOBALS.last_update = GLOBALS.boot_time
    
    boot_userdb()
    boot_db()

    log.info('Starting server on port %s', GLOBALS.PORT)

    server = TelnetServer(port=GLOBALS.PORT, timeout=.05)
    # set our own hooks for welcome/disconnect messaging
    server.on_connect = connect_hook
    server.on_disconnect = disconnect_hook

    log.info('Starting event queue')
    GLOBALS.Scheduler = EventQueue()
    # Must be called BEFORE scheduling any events
    update_game_time()
    GLOBALS.Scheduler.add(delay=20, realtime=True, callback=log.debug, args=['--MARK--'], repeat=-1)
    GLOBALS.Scheduler.add(delay=300, realtime=True, callback=update_snapshot, args=[], repeat=-1)
    #GLOBALS.Scheduler.add(delay=600, realtime=True, callback=log_objgraph, args=[], repeat=-1)

    loop_count = 0
    while GLOBALS.GAME_RUNNING:
        # Tick / run game here
        loop_start = time.time()
        server.poll()
        kick_idlers()
        process_commands()
        #update()
        send_prompts()
        update_game_time()
        GLOBALS.Scheduler.tick()
        loop_end = time.time()
        loop_count += 1
        if loop_count % 1000 == 0:
            log.debug('Loop time: %7.5f, total loops: %s', (loop_end - loop_start), loop_count)

    log.info('Server shutdown received')
    sync_db(force=True)

if __name__ == '__main__':
    main()
