"""
Player/NPC races
"""


class Race(object):
    """Race entity"""
    def __init__(self, name):
        self.name = name
        self.player_type = True
        self.description = None
        self._stats = {}
        self._max_stats = {}
