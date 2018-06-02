"""
BaseActor class - base class for NPC and Players
"""
import copy as copy
from utils import log

_def_profile = {
    'name':   '',
    'gender': '',
    'race':   '',
    'class':  '',
    'age':    ''
}

_def_stats = {
    'hp':    0,
    'maxhp': 0,
    'mp':    0,
    'maxmp': 0,
    'level': 1,
    'xp':    0,
    'armor': 0,
    'money': 0
}

_def_attributes = {
    'strength':  0,
    'intellect': 0,
    'dexterity': 0,
    'stamina':   0,
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
        
        # Hold basic player info (name, gender, race, class)
        self._profile = copy.copy(_def_profile)

        # Holds current actor state (hp, armor, xp, strength)
        self._stats = copy.copy(_def_stats)

        # Hold player traits (strength, intellect, etc)
        self._attributes = copy.copy(_def_attributes)

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
            elif k in self._profile:
                log.debug(' +-> adding profile {}={}'.format(k, v))
                try:
                    self._profile[k] = int(v)
                except (ValueError, KeyError) as e:
                    log.error(' +-> XX Adding profile FAILED: {}={}: {}'.format(k, v, e))


    def get_name(self):
        return self._profile['name']


    def get_race(self):
        return self._profile['race']


    def get_gender(self):
        return self._profile['gender']


    def get_class(self):
        return self._profile['class']



