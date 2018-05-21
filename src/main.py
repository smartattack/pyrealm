"""
PyRealm
"""


from character import Character
from location import Location
from server import Server
from player import Player
from constants import *

import time
import logging

def handle_sockets(mud, players):

    # Update socket states
    mud.update()

    # Handle new connections
    for id in mud.get_new_players():

        # Create a new player object for this connection id
        players[id] = Player()
        players[id].name = "connecting_%d" % id  # temporary name
        players[id].tell(WELCOME_BANNER)
        mudlog.info('Player {} connected'.format(players[id].name))
        print ("Connected: {}".format(players[id].maxhp))

    # Handle disconnected players/sockets
    for id in mud.get_disconnected_players():

        if id not in players:
            continue

        # Tell all players about the disconnect

        # Remove the id from the players dict
        del(players[id])

    # Handle input from players
    for id, line in mud.get_input():

        if id not in players:
            continue

        players[id].input = line


def send_to_players(mud, players):
    # Push output to players
    for id in players:
        if players[id].output:
            mud.send_message(id, players[id].output)
            players[id].output = ""


def process_events():
    pass

def process_input(players):
    for id in players:
        if players[id].input:
           players[id].output = "|%s|" % players[id].input

def main():

    mudlog = logging.getLogger('mudlog')
    mudlog.setLevel(logging.DEBUG)
    fh = logging.FileHandler('mud.log')
    fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s'))
    mudlog.addHandler(fh)
    
    mudlog.info("Starting Server()")
    mud = Server()
    players = {}
    events = []


    while True:

        handle_sockets(mud, players)
        process_input(players)
        process_events()
        send_to_players(mud, players)
        time.sleep(0.1)



if __name__ == "__main__":
    main()
