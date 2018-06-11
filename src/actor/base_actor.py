"""
BaseActor class - base class for NPC and Players
"""
import copy as copy
from utils import log

_DEF_STATS = {
    'hp':    0,
    'maxhp': 0,
    'mp':    0,
    'maxmp': 0,
    'level': 1,
    'xp':    0,
    'armor': 0,
    'money': 0
}

_DEF_ATTRIBUTES = {
    # Determines carry capacity, strength of attacks
    'strength':  0,
    # Affects skill learning, MP leveling
    'intellect': 0,
    # points per level, MP
    'wisdom':    0,
    # Increases likelihood of hit, dodging, critical hits
    'dexterity': 0,
    # base HP, regen rates
    'stamina':   0,
    # Affects buy/sell rates, likelihood of NPCs to attack
    'charisma':  0
}


class BaseActor(object):
    """BaseActor is responsible for holding general settings that apply
    to both NPC and Players.
    Don't call directly
    """

    def __init__(self):
        self.location = None
        self.is_player = False
        
        self._name = 'nobody'
        self._gender = 'M'
        self._class = ''
        self._race = ''
        
        # Holds current actor state (hp, armor, xp, strength)
        self._stats = copy.copy(_DEF_STATS)

        # Hold player traits (strength, intellect, etc)
        self._attributes = copy.copy(_DEF_ATTRIBUTES)

        # inventory, dict:  k=item, v=count
        self._carried = {}

        # items worn or wielded, dict: k=slot, v=item
        self._worn = {}


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
            else:
                log.error(' +-> ?? Unknown argument: {}={}'.format(k, v))


    def get_attribute(self, name):
        """Return attribute value"""
        try:
            return self._attributes[name]
        except (KeyError, AttributeError) as e:
            log.error('Undefined attribute: {}'.format(e))
            return None


    def get_stat(self, name):
        """Return stats value"""
        try:
            return self._stats[name]
        except (KeyError, AttributeError) as e:
            log.error('Undefined stat: {}'.format(e))
            return None


    def get_name(self):
        return self._name


    def set_name(self, name):
        self._name = name


    def get_race(self):

        return self._race


    def set_race(self, race):
        self._race = race


    def get_gender(self):
        return self._gender


    def set_gender(self, gender):
        self._gender = gender


    def get_class(self):
        return self._class


    def set_class(self, pclass):
        self._class = pclass
