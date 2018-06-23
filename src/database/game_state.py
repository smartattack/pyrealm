"""
Persists game state across restarts.
"""

class GameState(object):
    """Holds global game persistence info"""
    def __init__(self):
        """Only runs on first boot"""
        self._runtime = 0.0
        self._max_instance = 0
    
    def post_init(self):
        """Needed by load_from_json"""
        pass

    @property
    def runtime(self):
        return self._runtime

    def add_runtime(self, seconds):
        self._runtime += seconds

    @property
    def max_instance(self):
        return self._max_instance
    
    @max_instance.setter
    def max_instance(self, number):
        self._max_instance = number