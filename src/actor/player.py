"""
Player is an actor being played by a connected user
"""

from utils import log
from actor.base import BaseActor

class Player(BaseActor):
    """Player class - holds information about player characters"""

    def __init__(self, client):
        BaseActor.__init__(self)
        # This might not be needed - we can probably check
        # if the object is of subclass Player or NPC instead
        self.is_player = True
        self.client = client

        # Ability to perform various tasks or skills
        # Some abilities are granted by class/race
        self._abilities = set()


    def send(self, msg):
        """Send a message to player, supports color codes"""
        self.client.send_cc(msg)


    def send_wrapped(self, msg):
        """Send wrapped text to player, supports color codes"""
        self.client.send_wrapped(msg)


    def send_raw(self, msg):
        """Send raw string to player, no color support"""
        self.client.send_raw(msg)         


    def add_ability(self, ability):
        log.debug('Adding "{}" ability to player {}'.format(ability, self._profile['name']))
        self._abilities.add(ability)


    def remove_ability(self, ability):
        log.debug('Removing "{}" ability from player {}'.format(ability, self._profile['name']))
        self._abilities.remove(ability)


    def clear_abilities(self):
        log.debug('Removing all abilities from player {}'.format(self._profile['name']))
        self._abilities = set()


    def has_ability(self, ability):
        if ability in self._abilities:
            return True
        else:
            return False


    def list_abilities(self):
        return list(self._abilities)