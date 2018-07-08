"""
Base Item class
"""

from utils import log
from game_object import GameObject, InstanceRegistry
import globals as GLOBALS


def find_room(location):
    """Return Room object matching location vnum"""
    if location is None:
        return None
    for vnum, room in GLOBALS.rooms.items():
        if location == room.vnum:
            return room
    else:
        return None


class BaseItem(GameObject):
    """All items will derive from this class"""
    def __init__(self, name, description, short_desc, **kwargs):
        log.debug("BaseItem.__init__(name=%s, short_desc=%s)", name, short_desc)
        log.debug("BaseItem.__mro__ = %s", BaseItem.__mro__)
        GameObject.__init__(self, name=name, description=description,
                            short_desc=short_desc)
        self._weight = 0
        self._cost = 0
        self.carried_by = None
        self.worn_by = None
        log.debug('Registering item %s with instances.all_items', self.gid)
        GLOBALS.all_items[self.gid] = self

    def post_init(self):
        """This init gets called after a load from disk.  It reconstitutes missing data"""
        pass

    @property
    def weight(self):
        return self._weight
    
    @property
    def cost(self):
        return self._cost
    
    @cost.setter
    def cost(self, amount):
        self._cost = amount

    def add_to_room(self, location):
        """Add item to a room"""
        room = find_room(location)
        if room:
            if self.carried_by:
                # FIXME: vnum needs to convert to a gid instance id
                log.warning('Item %s is carried by %s, cannot add to room %s',
                            self.vnum, self.carried_by, location)
            else:
                room.add_item(self)        


    def add_to_actor(self, actor):
        """Add item to actor inventory"""
        #actor.add_item(self)
        self.carried_by = actor.gid


    def equip_to_actor(self, actor):
        """Add item to actor wear slot"""
        #FIXME: check if actor has open matching wear slot"""
        self.worn_by = actor.gid


class Container(GameObject):
    """Base container item"""
    def __init__(self):
        pass
