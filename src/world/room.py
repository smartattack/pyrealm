"""
Room Class
"""

class Room(object):
    """
    A room is basically a container object
    """

    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self._outside = None
        self.actors = []
        self.exits = {}
    
    def __repr__(self):
        return 'Room object, id={}, name={}'.format(self.id, self.name)
