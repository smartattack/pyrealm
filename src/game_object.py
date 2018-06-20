"""
Game Object - base of all tracked game objects
"""

import time

class GameObject(object):
    """All serializable and tracked game objects extend this class"""
    # This list gets processed by to_json() and anything in it will
    # not be serialized in save game data.  Subclasses add to this
    # list.
    _skip_list = ['_checksum', '_last_save']

    def __new__(cls, *args, **kwargs):
        """Custom new() to ensure we get a unique ID"""
    
    def __init__(self, name=None, description=None, short_desc=None, **kwargs):
        self._name = name
        self._description = description
        self._short_desc = short_desc
        if 'skip_list' in kwargs:
            if isinstance(kwargs['skip_list']):
                self._skip_list += kwargs['skip_list']
        # Update checksum / last_saved
        self._init_accounting()
    
    def _init_accounting(self):
        """Initialize checksum and last_saved vars"""
        self.checksum = ''
        self._last_saved = time.time()
