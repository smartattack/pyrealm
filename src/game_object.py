"""
Game Object - Base for all trackable game entities
"""

import time
import copy as copy
from weakref import WeakValueDictionary
from world.room import *
from utils import log, wrap_one_line
from miniboa.xterm import word_wrap as miniboa_wrap
import globals as GLOBALS


class GameObject():
    """All serializable and tracked game objects extend this class"""
    # This list gets processed by to_json() and anything in it will
    # not be serialized in save game data.  Subclasses add to this
    # list.
    _skip_list = set()
    _skip_list.update(['_checksum', '_last_save'])

    def __new__(cls, *args, **kwargs):
        """Custom new() to ensure we get a unique ID"""
        log.debug("FUNC GameObject.new()")
        # This bit of magic runs when we load from disk and makes sure
        # we initialize everything properly
        this = super().__new__(cls)
        InstanceRegistry.track(this)
        return this
    
    def __init__(self, name=None, description=None, short_desc=None, **kwargs):
        log.debug('Inside GameObject.init(%s, %s, %s)', name, description, short_desc)
        self.name = name
        self.description = description
        self.short_desc = short_desc
        if 'skip_list' in kwargs:
            if isinstance(kwargs['skip_list'], list):
                self._skip_list.update(kwargs['skip_list'])
        # Update checksum / last_saved
        self._init_accounting()
    
    def _init_accounting(self):
        """Initialize checksum and last_saved vars"""
        self.checksum = ''
        self._last_saved = time.time()
    
    
    def post_load_init(self):
        """Override this with any code that needs to run after load from disk"""
        pass


class InstanceRegistry():
    """Creates and tracks unique IDs for all tracked objects"""
    gid = 0
    all_instances = WeakValueDictionary()
    all_items = WeakValueDictionary()
    all_actors = WeakValueDictionary()
    all_locations = WeakValueDictionary()

    @classmethod
    def track(cls, instance):
        """Increment and return an instance id"""
        InstanceRegistry.gid += 1
        GLOBALS.game_state.gid = InstanceRegistry.gid
        instance.gid = InstanceRegistry.gid
        log.debug('Adding instance %s to all_instances', cls.gid)
        InstanceRegistry.all_items[cls.gid] = instance
        if isinstance(instance, BaseItem):
            log.debug('Adding all_items[%s] = %s', cls.gid, instance)
            InstanceRegistry.all_items[cls.gid] = instance
        elif isinstance(instance, BaseActor):
            log.debug('Adding all_actors[%s] = %s', cls.gid, instance)
            InstanceRegistry.all_actors[cls.gid] = instance
        elif isinstance(instance, Room):
            log.debug('Adding all_locations[%s] = %s', cls.gid, instance)
            InstanceRegistry.all_locations[cls.gid] = instance
        else:
            log.warn('Unknown instance type: %s: %s', cls.gid, type(instance))


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


class BaseActor(GameObject):
    """BaseActor is responsible for holding general settings that apply
    to both NPC and Players.
    Don't call directly
    """

    def __init__(self, name='Nobody', description='None', **kwargs):
        self.location = None
        self.is_player = False
        
        self._gender = 'M'
        self._race = ''
        
        # Holds current actor state (hp, armor, xp, strength)
        self._stats = copy.copy(_DEF_STATS)

        # Hold player traits (strength, intellect, etc)
        self._attributes = copy.copy(_DEF_ATTRIBUTES)

        # inventory, dict:  k=item, v=count
        self._carried = {}

        # items worn or wielded, dict: k=slot, v=item
        self._worn = {}

        self._skip_list = ['client', '_last_saved', '_checksum']


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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, race):
        self._race = race

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender



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
        self._weight = 0
        self._cost = 0
        self.carried_by = None
        GameObject.__init__(self, name=name, description=description,
                            short_desc=short_desc, skip_list=['carried_by'])

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
                            self.vnum, self.carried_by.name, location)
            else:
                room.add_item(self)        

    def add_to_actor(self, actor):
        """Add item to actor inventory"""
        #actor.add_item(self)
        self.carried_by = actor

class Container(GameObject):
    """Base container item"""
    def __init__(self):
        pass

# Create object registry used for global object tracking
instances = InstanceRegistry()


class Room(GameObject):
    """
    A room is basically a container object
    """
    vnum = None

    def __init__(self, vnum=None, name=None, description=None,
                 outside=None, exits=None):
        """NOTE: I am not called on objects loaded from disk."""
        log.debug("Inside Room.init()")
        super().__init__(name=name, description=description,
                            skip_list=['actors', 'inventory'])
        # vnum is used by exits
        self.vnum = vnum
        self._outside = outside
        self.inventory = []
        self.actors = []
        self.exits = {}
        if exits:
            self.exits = exits
        log.debug('Room created: %s', self.__repr__())


    def post_init(self):
        """This init gets called after a load from disk.  It reconstitutes missing data"""
        self.actors = []
        self.inventory = []
        self._skip_list.update(['actors','inventory'])


    def __repr__(self):
        return 'Room object, vnum={}, name={}'.format(self.vnum, self.name)


    def is_outside(self):
        """Return true if outside(affected by daylight)"""
        if self._outside:
            return True
        else:
            return False


    def add_actor(self, act):
        """Add a character to a room"""
        log.debug('FUNC Room.add_actor(%s) -> %s', act.name, self.vnum)
        if not act in self.actors:
            log.debug('Adding %s to room %s', act.name, self.vnum)
            self.actors.append(act)
            # Don't send to NPCs
            if hasattr(act, 'send'):
                act.send(self.show_info(act.client.columns))


    def remove_actor(self, act):
        """Remove character from room"""
        log.debug('FUNC Room.remove_actor()')
        if act in self.actors:
            log.debug('Removing %s from room %s', act.name, self.vnum)
            self.actors.remove(act)


    def add_item(self, item):
        """Add an item to room inventory"""
        if not isinstance(item, BaseItem):
            log.warning('Tried to add %s as an item, type is %s',
                        item, type(item))
            return
        self.inventory.append(item)

    def remove_item(self, item):
        """Remove an item from room inventory"""
        if item in self.inventory:
            log.debug('Removing {} from room {} inventory',
                      item.name, self.vnum)
            self.inventory.remove(item)
        else:
            log.warning('Did not find item %s in room %s inventory',
                        item.name, self.vnum)


    def _exitstr(self, direction):
        """Show an exit on small map"""
        log.debug('FUNC _exit_str(%s)', direction)
        output = None
        if direction in self.exits:
            log.debug('%s', self.exits[direction])
            return '^c{}^d'.format(dir_name(direction, map=True))
        else:
            return ''


    def show_exits(self):
        """Return stringified exits"""
        exits = []
        for exit in self.exits:
            log.debug('EXIT == %s, dir_name(exit) == %s', exit, dir_name(exit))
            exits.append('^G{}^d'.format(dir_name(exit)))
        log.debug('EXIT == %s', exits)
        return '^WExits: ^w[^G' + ', '.join(map(str, exits)) + '^w].^d\n\n'


    def show_info(self, width=70):
        """Show room name, exit map, description"""
        log.debug('FUNC show_info(%s)', width)
        swidth = width - 15
        output = '^W{}^d{}   {}  {}\n'.format(
                                self.name.ljust(swidth, ' '),
                                self._exitstr(DIR_NORTHWEST).ljust(2, ' '),
                                self._exitstr(DIR_NORTH).ljust(2,' '),
                                self._exitstr(DIR_NORTHEAST).ljust(2, ' '))
        output += '^w{}^d{}^w--{}^w(^Y*^w){}^w--{}\n'.format(
                                                '-'.ljust(swidth, '-'),
                                self._exitstr(DIR_WEST).ljust(1, '-'),
                                self._exitstr(DIR_UP).ljust(1, '-'),
                                self._exitstr(DIR_DOWN).ljust(1, '-'),
                                self._exitstr(DIR_EAST).ljust(1, '-'))
        (first_line, remaining) = wrap_one_line(self.description, swidth)
        output += '^g{}^d{}   {}  {}\n'.format(
                                first_line.ljust(swidth, ' '),
                                self._exitstr(DIR_SOUTHWEST).ljust(2, ' '),
                                self._exitstr(DIR_SOUTH).ljust(2,' '),
                                self._exitstr(DIR_SOUTHEAST).ljust(2, ' '))
        if remaining:
            log.debug("REMAINING=|%s|", remaining)
            remaining = '\n'.join(miniboa_wrap(remaining, width, indent=0, 
                                              padding=0)).lstrip()
            output += '^g{}^d\n'.format(remaining)
        items = []
        for item in self.inventory:
            items.append(item.short_desc)
        if items:
            output += '^wItems here:\n^M' + '^w, ^M'.join(items) + '\n^d'
        return output