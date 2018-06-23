"""
Game Object - base of all tracked game objects
"""

import time
from utils import log

class GameObject(object):
    """All serializable and tracked game objects extend this class"""
    # This list gets processed by to_json() and anything in it will
    # not be serialized in save game data.  Subclasses add to this
    # list.
    _skip_list = set()
    _skip_list.update(['_checksum', '_last_save'])

    def __new__(cls, *args, **kwargs):
        """Custom new() to ensure we get a unique ID"""
        log.debug("Inside GameObject.new()")
        # This bit of magic runs when we load from disk and makes sure
        # we initialize everything properly
        this = super().__new__(cls)
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
