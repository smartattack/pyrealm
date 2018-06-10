"""
User utility functions
"""

import globals as GLOBALS
from actor.player import Player


def user_online(username):
    """Check if a given username is logged in"""
    if username:
        for user in GLOBALS.players.values():
            if user.username == username:
                return True
    return False


def broadcast(msg: str):
    """Send a message to all connected clients"""
    if msg is not None:
        for c in GLOBALS.clients:
            c.send(msg)


def send_all(ch: Player, msg: str):
    """Send a message to all other players"""
    if msg is not None:
        for user in GLOBALS.players.values():
            if user.player != ch:
                user.send(msg)
