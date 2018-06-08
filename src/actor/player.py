"""
Player is an actor being played by a connected user
"""

from utils import log, from_json, to_json
from actor.base_actor import BaseActor
import globals as GLOBALS
import os
import time
import hashlib
import jsonpickle
import json


class Player(BaseActor):
    """Player class - holds information about player characters"""

    def __init__(self, client):
        BaseActor.__init__(self)
        # This might not be needed - we can probably check
        # if the object is of subclass Player or NPC instead
        self.is_player = True
        self._client = client
        self._checksum = None

        # Ability to perform various tasks or skills
        # Some abilities are granted by class/race
        self._abilities = set()


    def send(self, msg):
        """Send a message to player, supports color codes"""
        self._client.send_cc(msg)


    def send_wrapped(self, msg):
        """Send wrapped text to player, supports color codes"""
        self._client.send_wrapped(msg)


    def send_raw(self, msg):
        """Send raw string to player, no color support"""
        self._client.send_raw(msg)         


    def add_ability(self, ability):
        log.debug('Adding "{}" ability to player {}'.format(ability, self._name))
        self._abilities.add(ability)


    def remove_ability(self, ability):
        log.debug('Removing "{}" ability from player {}'.format(ability, self._name))
        self._abilities.remove(ability)


    def clear_abilities(self):
        log.debug('Removing all abilities from player {}'.format(self._name))
        self._abilities = set()


    def has_ability(self, ability):
        if ability in self._abilities:
            return True
        else:
            return False


    def list_abilities(self):
        return list(self._abilities)

    
    def save(self):
        """Write to disk"""
        log.debug('FUNC: Player.save()')
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.PLAYER_DIR)    
        try:
            os.makedirs(pathname, 0o755, True)
        except Exception as e:
            log.critical('Failed to create directory: {} -> {}'.format(pathname, e))
        #data = json.dumps(self, default = to_json, indent=4, sort_keys=True)
        data = jsonpickle.encode(self, unpicklable=False)
        print(json.dumps(data, indent=4))
        checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
        if self._checksum != checksum:
            self._checksum = checksum
            self._last_saved = time.time()
            log.info('Saving player: {}'.format(self.get_name()))
            filename = os.path.join(pathname, self.get_name().lower() + '.json')
            with open(filename, "w") as f:
                f.write(json.dumps(json.loads(data), indent=4))
    

    def load(self, username):
        """Load from disk"""
        if not username:
            log.error('Attempted to call Player.load without a username!')
            raise KeyError('Must include a username with load()')
        filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.PLAYER_DIR, username.lower() + '.json')
        with open(filename, "r") as f:
            data = f.readlines()
        loaded = jsonpickle.decode(data)
        #loaded = json.loads(data, object_hook = from_json)
        if isinstance(loaded, Player):
            # Avoid resaving right away
            self._last_saved = time.time()
            self._checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
            return loaded
        else:
            logger.warning('Could not load player from file: {}'.format(username.lower()))