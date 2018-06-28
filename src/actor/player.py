"""
Player is an actor being played by a connected user
"""

from utils import log
from utils import xp_to_level, stat_color
from actor.base_actor import BaseActor
from game_object import InstanceRegistry
import globals as GLOBALS


# Positions - these are parsed in the user command handler
# Move to globals?
Positions = ('dead', 'sleeping', 'sitting', 'fighting', 'standing')

class Player(BaseActor):
    """Player class - holds information about player characters"""

    def __init__(self):
        """Not called on load_from_json, but from Player() during login"""

        # Initialize BaseActor.  This must be here to register instance with
        # all_actors, and BaseActor also calls super.__init__() which generates
        # the instance's gid.  Keep me first so we can override values below.
        super().__init__(self)

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

        # Make sure we don't serialize client structure!
        self._skip_list.update(['client'])

        # Add to global dictionaries
        InstanceRegistry.track(self)
        log.debug('Registering player %s with instances.all_players')
        GLOBALS.all_players[self.gid] = self


    def post_init(self):
        """Called after load_from_json deserializes the structure.  Fills in
        missing important bits"""
        self._skip_list.update(['client'])
        self.client = None


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
