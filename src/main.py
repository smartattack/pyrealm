"""
PyRealm
"""

import logging
import time
import constants

from player import Player
# from character import Character
# from location import Location
from server import Server
from login import *
from command import *
import db

def handle_sockets(mud, players):
    """Process Sockets - called from within game loop"""

    # Update socket states
    mud.update()

    # Handle new connections
    for idx in mud.get_new_players():
        # Create a new player object for this connection idx
        players[idx] = Player()
        players[idx].cid = idx  # Allow us to call tell later
        players[idx].send_now = mud.send_no_newline
        players[idx].mud = mud
        players[idx].name = "connecting_%d" % idx  # temporary name
        players[idx].send_now(idx, constants.WELCOME_BANNER)
        players[idx].state = Player._PLAYER_USERNAME
        mudlog.info("Player {} connected".format(players[idx].name))
        print("Connected: {}".format(players[idx].maxhp))

    # Handle disconnected players/sockets
    for idx in mud.get_disconnected_players():

        if idx not in players:
            continue

        # Tell all players about the disconnect

        # Remove the idx from the players dict
        del players[idx]

    # Handle input from players
    for idx, line in mud.get_input():

        if idx not in players:
            continue

        players[idx].input = line


def send_to_players(mud, players):
    """Push output to players"""

    for idx in players:
        if players[idx].output:
            mud.send_message(idx, players[idx].output)
            players[idx].output = ""


def process_events():
    """Event queue processor"""
    pass


def process_input(players):
    """Handles input from players"""
    for idx in players:
        if players[idx].input:
            # State machine to determine whether to dispatch login or command
            if players[idx].state == Player._PLAYER_PLAYING:
                command_handler(players[idx])
            else:
                login_handler(players[idx])
            # Clear input after handlers have done processing
            players[idx].input = None
            players[idx].command = None
            players[idx].args = None


def handle_disconnects(players):
    """Clean up disconnected players"""
    # FIXME: do we want to do this after a timeout?
    # Maybe a body should stay around, at least.

    disconnected_players = []
    for idx, player in list(players.items()):
        if player.state == Player._PLAYER_DISCONNECT:
            disconnected_players.append(idx)
    for i in disconnected_players:
        mudlog.info("Deleting players[{}] ({})".format(i, players[i].name))
        del players[i]


def main():
    """Main entry point"""

    global mudlog
    mudlog = logging.getLogger('mudlog')
    mudlog.setLevel(logging.DEBUG)
    fh = logging.FileHandler(constants.logfile)
    fh.setFormatter(
        logging.Formatter('%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s'))
    mudlog.addHandler(fh)

    # Initialize database
    db.check_db()

    mud = Server()
    mudlog.info("Starting Server()")
    mud.start()

    players = {}
    # events = []

    while True:
        # Do socket polling
        handle_sockets(mud, players)

        # Handle player input
        process_input(players)

        # Process event queue
        process_events()

        # Clean-up disconnected players
        handle_disconnects(players)

        # Process output to players
        send_to_players(mud, players)

        # Sleep to avoid pinning cpu
        time.sleep(0.05)


if __name__ == "__main__":
    main()
