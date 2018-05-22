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


def handle_sockets(mud, players):
    '''Process Sockets - called from within game loop'''

    # Update socket states
    mud.update()

    # Handle new connections
    for idx in mud.get_new_players():
        # Create a new player object for this connection idx
        players[idx] = Player()
        players[idx].name = "connecting_%d" % idx  # temporary name
        players[idx].tell(constants.WELCOME_BANNER)
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
    '''Push output to players'''

    for idx in players:
        if players[idx].output:
            mud.send_message(idx, players[idx].output)
            players[idx].output = ""

def process_events():
    '''Event queue processor'''
    pass

def process_input(players):
    """Handles input from players"""
    for idx in players:
        if players[idx].input:
            players[idx].output = "|%s|" % players[idx].input


def main():
    """Main entry point"""

    global mudlog
    mudlog = logging.getLogger('mudlog')
    mudlog.setLevel(logging.DEBUG)
    fh = logging.FileHandler(constants.logfile)
    fh.setFormatter(
        logging.Formatter('%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s'))
    mudlog.addHandler(fh)

    mudlog.info("Starting Server()")
    mud = Server()
    players = {}
    #events = []

    while True:
        handle_sockets(mud, players)
        process_input(players)
        process_events()
        send_to_players(mud, players)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
