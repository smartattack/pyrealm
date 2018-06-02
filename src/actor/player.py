"""
Player is an in-game character played by a user
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

    def update(self, **kwargs):
        """Update one or many attributes/stats/profile of a player"""
        log.debug('Called player.update():')
        for k,v in kwargs.items():
            if k in self._stats:
                log.debug(' +-> adding stats {}={}'.format(k, v))
                try:
                    self._stats[k] = int(v)
                except (ValueError, KeyError) as e:
                    log.error(' +-> XX Adding stats FAILED: {}={}: {}'.format(k, v, e))
            elif k in self._attributes:
                log.debug(' +-> adding attribute {}={}'.format(k, v))
                try:
                    self._attributes[k] = int(v)
                except (ValueError, KeyError) as e:
                    log.error(' +-> XX Adding attribute FAILED: {}={}: {}'.format(k, v, e))
            elif k in self._profile:
                log.debug(' +-> adding profile {}={}'.format(k, v))
                try:
                    self._profile[k] = int(v)
                except (ValueError, KeyError) as e:
                    log.error(' +-> XX Adding profile FAILED: {}={}: {}'.format(k, v, e))          

    def add_ability(self, ability):
        self._abilities.add(ability)

    def remove_ability(self, ability):
        self._abilities.remove(ability)

    def clear_abilities(self):
        self._abilities = set()

    def has_ability(self, ability):
        if ability in self._abilities:
            return True
        else:
            return False

    def list_abilities(self):
        return list(self._abilities)