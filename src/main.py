"""
PyRealm
"""


from character import Character
from constants import *
from server import Server
from player import Player
from log import Logger

import time


def handle_sockets(mud, players):

    # Update socket states
    mud.update()

    # Handle new connections
    for id in mud.get_new_players():

        # Create a new player object for this connection id
        players[id] = Player()

        mud.send_message(id, WELCOME_BANNER)

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
        print ("Player %s input == |%s|".format(id, line))

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

    mudlog = Logger(logfile)

    mudlog.add("Starting Server()")
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
