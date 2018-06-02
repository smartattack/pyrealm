"""
BaseActor class - base class for NPC and Players
"""
import copy.copy as copy
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
        self._profile = copy(_def_profile)

        # Holds current actor state (hp, armor, xp, strength)
        self._stats = copy(_def_stats)

        # Hold player traits (strength, intellect, etc)
        self._attributes = copy(_def_attributes)

        # inventory, dict:  k=item, v=count
        self._carried = {}

        # items worn or wielded, dict: k=slot, v=item
        self._worn = {}



    """
    FIXME: Do I need setters in here at all?
    Maybe a derivative class has to implement setters,
    especially for attributes/profile/stats
    """

    def get_name(self):
        return self._profile['name']

    def set_name(self, name):
        self._profile['name'] = name

    def get_race(self):
        return self._profile['race']

    def set_race(self, race):
        self._profile['race'] = race

    def get_gender(self):
        return self._profile['gender']

    def set_gender(self, gender):
        self._profile['gender'] = gender

    def get_class(self):
        return self._profile['class']

    def set_class(self, class):
        self._profile['class'] = class


