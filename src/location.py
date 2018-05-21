"""
Location - a location in the world.
Container which has livings and items.
"""

import logging
mudlog = logging.getLogger('mudlog')

class Location:
    # Highest vnum so far - auto-increments
    _sequence = 0

    def __init__(self, name: str, desc: str=None, vnum=None):
        if vnum:
            self._vnum = vnum
            if vnum > self._sequence:
                Location._sequence = vnum
        else:
            self._vnum = self._sequence
        Location._sequence += 1
        self.name = name
        self.desc = desc
        self.items = set()
        self.players = set()
        self.exits = {}

    def destroy(self):
        for player in self.players:
            if player.location is self:
                player.location = _limbo
        self.players.clear()
        self.items.clear()
        self.exits.clear()

    def notify_player_arrived(self, player):
        pass

    def notify_player_left(self, player):
        pass

# Define default room for player creation
_limbo = Location(name='Limbo', desc='The Construct', vnum=0)
