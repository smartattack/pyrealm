"""
Game Object - Base for all trackable game entities
"""

import time
from utils import log
import globals as GLOBALS


class GameObject():
    """All serializable and tracked game objects extend this class"""
    # This list gets processed by to_json() and anything in it will
    # not be serialized in save game data.  Subclasses add to this
    # list.
    _skip_list = set()
    _skip_list.update(['_checksum', '_last_saved'])


    def __new__(cls, *args, **kwargs):
        """Custom new() to ensure we get a unique ID"""
        log.debug("FUNC GameObject.new()")
        # This bit of magic runs when we load from disk and makes sure
        # we initialize everything properly
        this = super().__new__(cls)
        return this


    def __init__(self, name=None, description=None, short_desc=None, **kwargs):
        log.debug('Inside GameObject.init()')
        self.name = name
        # Description used in inventory, on the ground
        self.description = description
        self.short_desc = short_desc
        if 'skip_list' in kwargs:
            if isinstance(kwargs['skip_list'], list):
                self._skip_list.update(kwargs['skip_list'])
        InstanceRegistry.track(self)
        # Update checksum / last_saved
        self._init_accounting()


    def _init_accounting(self):
        """Initialize checksum and last_saved vars"""
        self._checksum = ''
        self._last_saved = time.time()


    def post_load_init(self):
        """Override this with any code that needs to run after load from disk"""
        pass


class InstanceRegistry():
    """Creates and tracks unique IDs for all tracked objects"""
    gid = 0

    @classmethod
    def track(cls, instance):
        """Increment and return an instance id"""
        log.debug('BEFORE InstanceRegistry.gid=%s', cls.gid)
        if cls.gid in GLOBALS.all_instances:
            log.warning('GID %s in all_instances, finding next available gid',
                        cls.gid)
            while cls.gid in GLOBALS.all_instances:
                cls.gid += 1
        else:
            cls.gid += 1
        # Sync game_state.max_gid so we don't overwrite gids
        # on boot.
        GLOBALS.game_state.max_gid = cls.gid
        instance.gid = cls.gid
        log.debug('Adding instance %s to instances.all_instances', instance.gid)
        GLOBALS.all_items[instance.gid] = instance


# Initialize instance registry for tracking
instances = InstanceRegistry()
