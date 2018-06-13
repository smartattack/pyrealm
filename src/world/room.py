"""
Room Class
"""

from utils import log
from actor.player import Player
import globals as GLOBALS

# Used by exits.  Compatible with Merc
DIR_NORTH     = 0
DIR_EAST      = 1
DIR_SOUTH     = 2
DIR_WEST      = 3
DIR_UP        = 4
DIR_DOWN      = 5
DIR_NORTHEAST = 6
DIR_NORTHWEST = 7
DIR_SOUTHEAST = 8
DIR_SOUTHWEST = 9
DIR_SOMEWHERE = 10

DIR_NAMES = {
    0:'North',
    1:'East',
    2:'South',
    3:'West',
    4:'Up',
    5:'Down',
    6:'Northeast',
    7:'Northwest',
    8:'Southeast',
    9:'Southwest',
    10:'nothingness'
}

DIR_FROM_NAMES = {
    0:'South',
    1:'West',
    2:'North',
    3:'East',
    4:'Down',
    5:'Up',
    6:'Southwest',
    7:'Southeast',
    8:'Northwest',
    9:'Northeast',
    10:'thin air'
}

class Room(object):
    """
    A room is basically a container object
    """

    def __init__(self, id=None, name=None, desc=None,
                 outside=None, exits=None):
        self.id = id
        self.name = name
        self.description = desc
        self._outside = outside
        self.actors = []
        self.exits = {}
        if exits:
            self.exits = exits
        log.debug('Room created: %s', self.__repr__())

    
    def __repr__(self):
        return 'Room object, id={}, name={}'.format(self.id, self.name)

    def is_outside(self):
        """Return true if outside(affected by daylight)"""
        if self._outside:
            return True
        else:
            return False


    def add_actor(self, act):
        """Add a character to a room"""
        log.debug('FUNC Room.add_actor()')
        if not act in self.actors:
            log.debug('Adding %s to room %s', act.get_name(), self.id)
            self.actors.append(act)
            if isinstance(act, Player):
                act.send('^Y{}^d\n^G{}^d\n'.format(self.name, self.description))


    def remove_actor(self, act):
        """Remove character from room"""
        log.debug('FUNC Room.remove_actor()')
        if act in self.actors:
            log.debug('Removing %s from room %s', act.get_name(), self.id)
            self.actors.remove(act)


GLOBALS.rooms[1] = Room(id=1, name='Entrance', desc='A lit entryway', outside=True,
                        exits={DIR_NORTH:{'to_room':2}})

GLOBALS.rooms[2] = Room(id=2, name='Courtyard', desc='An empty courtyard', outside=True,
                        exits={DIR_SOUTH:{'to_room':1}})