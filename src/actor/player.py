"""
Player is an actor being played by a connected user
"""

from utils import log
from actor.base_actor import BaseActor
import globals as GLOBALS
import os
import copy
import time
import hashlib
import jsonpickle
import json


class Player(BaseActor):
    """Player class - holds information about player characters"""

    def __init__(self):
        BaseActor.__init__(self)
        # This might not be needed - we can probably check
        # if the object is of subclass Player or NPC instead
        self.is_player = True

        # Set this later, we don't want it as a class attribute
        # since then it would get serialized
        self._client = None

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


    def _to_json(self, skip_list = None):
        """Create a Player() with select fields
        and serialize to JSON"""
        #for i in copylist:
        #    setattr(p, i, getattr(self, i))
        p = copy.copy(self)
        for i in skip_list:
            log.debug('skip_list: {}'.format(i))
            try:
                delattr(p, i)
            except:
                pass
        return jsonpickle.encode(p)


    def save(self):
        """Write to disk"""
        log.debug('FUNC: Player.save()')
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.PLAYER_DIR)    
        try:
            os.makedirs(pathname, 0o755, True)
        except Exception as e:
            log.critical('Failed to create directory: {} -> {}'.format(pathname, e))
        data = self._to_json(skip_list = ['_client','_checksum'])
        print(json.dumps(data, indent=4))
        checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
        if hasattr(self, '_checksum'):
            log.debug('Player.save(): Checking checksum for Player {}'.format(player.get_name()))
            if self._checksum != checksum:
                self._checksum = checksum
                self._last_saved = time.time()
        log.info('Saving player: {}'.format(self.get_name()))
        filename = os.path.join(pathname, self.get_name().lower() + '.json')
        with open(filename, "w") as f:
            f.write(json.dumps(json.loads(data), indent=4, sort_keys=True))
    

    def load(self, username):
        """Load from disk"""
        if not username:
            log.error('Attempted to call Player.load without a username!')
            raise KeyError('Must include a username with load()')
        filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.PLAYER_DIR, username.lower() + '.json')
        data = ''
        with open(filename, "r") as f:
            for line in f:
                data += line
        try:
            loaded = jsonpickle.decode(data)
        except Exception as e:
            log.error('Could not load Player data: {}'.format(e))
        if isinstance(loaded, Player):
            # Avoid resaving right away
            self._last_saved = time.time()
            self._checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
            return loaded
        else:
            log.error('loaded != Player()')
            raise IOError('Failed to load player data for {}'.format(username))