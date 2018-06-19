"""
Player is an actor being played by a connected user
"""

import os
import time
import hashlib
from utils import log, to_json, from_json, object_changed, make_checksum
from utils import xp_to_level, stat_color
from actor.base_actor import BaseActor
import globals as GLOBALS

# Positions - these are parsed in the user command handler
# Move to globals?
Positions = ('dead', 'sleeping', 'sitting', 'fighting', 'standing')

class Player(BaseActor):
    """Player class - holds information about player characters"""

    def __init__(self):
        BaseActor.__init__(self)
        # This might not be needed - we can probably check
        # if the object is of subclass Player or NPC instead
        self.is_player = True

        # Set this later, we don't want it as a class attribute
        # since then it would get serialized
        self.client = None

        # Ability to perform various tasks or skills
        # Some abilities are granted by class/race
        self._abilities = set()

        # Initialize to standing
        self.position = 'standing'

        # Tracks play time for this character
        self._playtime = 0

        self._checksum = None
        self._last_saved = None


    def __repr__(self):
        return 'Player({}) = {}'.format(self._name, self.__dict__)


    def send(self, msg):
        """Send a message to player, supports color codes"""
        self.client.send_cc(msg)


    def send_wrapped(self, msg):
        """Send wrapped text to player, supports color codes"""
        self.client.send_wrapped(msg)


    def send_raw(self, msg):
        """Send raw string to player, no color support"""
        self.client.send_raw(msg)


    def get_prompt(self):
        """Return a prompt for player"""
        # FIXME: only calc to_level when XP is changed, store in Player()  
        log.debug('FUN get_prompt()')
        hpcol = stat_color(self._stats['hp'], self._stats['maxhp'])
        mpcol = stat_color(self._stats['mp'], self._stats['maxmp'])
        to_level = xp_to_level(self._stats['level'], self._stats['xp'])
        prompt = '{}{}/{} ^chp {}{}/{} ^cmp ^m{}/{} ^cxp^w> ^d'.format(
            hpcol, self._stats['hp'], self._stats['maxhp'], 
            mpcol, self._stats['mp'], self._stats['maxmp'],
            self._stats['xp'], to_level)
        return prompt


    def add_ability(self, ability):
        """Add an ability to a player"""
        log.debug('Adding "%s" ability to player %s', ability, self._name)
        self._abilities.add(ability)


    def remove_ability(self, ability):
        """Remove an ability from a player"""
        log.debug('Removing "%s" ability from player %s', ability, self._name)
        self._abilities.remove(ability)


    def clear_abilities(self):
        """Remove all abilities from a player"""
        log.debug('Removing all abilities from player %s', self._name)
        self._abilities = set()


    def has_ability(self, ability):
        """Return bool if player has ability or not"""
        if ability in self._abilities:
            return True
        else:
            return False


    def list_abilities(self):
        """Return a list of all abilities for a player"""
        return list(self._abilities).sort()


    def save(self, logout=False):
        """Write to disk"""
        log.debug('FUNC: Player.save()')
        if logout:
            log.debug('+ Updating playtime for %s += %s', self.name, self.client.duration())
            # update playtime duration
            if hasattr(self, '_playtime'):
                self._playtime += self.client.duration()
            else:
                self._playtime = self.client.duration()
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.PLAYER_DIR)
        try:
            os.makedirs(pathname, 0o755, True)
        except OSError as err:
            log.critical('Failed to create directory: %s -> %s', pathname, err)
        data = to_json(self, skip_list=['client', '_checksum', '_last_saved'])
        checksum = make_checksum(data)
        if object_changed(self, checksum) or logout:
            self._checksum = checksum
            self._last_saved = time.time()
            log.info('Saving player: %s', self.name)
            filename = os.path.join(pathname, self.name.lower() + '.json')
            with open(filename, "w") as file:
                file.write(data)
                #log.debug('PLAYERDATA: {}'.format(data))


    def load(self, username):
        """Load from disk"""
        if not username:
            log.error('Attempted to call Player.load without a username!')
            raise KeyError('Must include a username with load()')
        filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.PLAYER_DIR, username.lower() + '.json')
        data = ''
        log.info('Loading Player(%s)', username)
        with open(filename, "r") as file:
            for line in file:
                data += line
        try:
            loaded = from_json(data)
        except Exception as err:
            log.error('Could not load Player data: %s', err)
        if isinstance(loaded, Player):
            # Avoid resaving right away
            self._last_saved = time.time()
            self._checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
            return loaded
        else:
            log.error('Loaded data != Player() - possible corruption')
            raise IOError('Failed to load player data for {}'.format(username))
