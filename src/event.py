"""
Event handler system
"""

from bisect import insort_right
import globals as GLOBALS
from utils import log
import time

class Event(object):
    """Basic single-fire event"""
    def __init__(self, delay, callback, args, realtime=False, repeat=0):
        """
        Create a single event, assumes delay is in game_time
        For cycling events, set repeat=-1, for N repeats, set repeat to nonzero
        """
        if realtime:
            self.due = GLOBALS.game_time + delay * GLOBALS.TIME_FACTOR
        else:
            self.due = GLOBALS.game_time + delay
        self.callback = callback
        self.args = args
        self.delay = delay
        self.repeat = repeat
        self.realtime = realtime
        self.active = True

    def __repr__(self):
        return 'event.Event object: {}'.format(self.__dict__)

    def __lt__(self, other):
        """Needed by insert/bisect"""
        return (self.due < other.due)

    def __gt__(self, other):
        """Needed by insert/bisect"""
        return (self.due > other.due)

    def __eq__(self, other):
        """Needed by insert/bisect"""
        return (self.due == other.due)

    def cancel(self):
        """Stop event from being triggered or scheduled"""
        self.active = False



class EventQueue(object):
    """Wraps a list of events and manages firing/scheduling"""
    def __init__(self):
        self._events = []
    
    def add(self, delay, callback, args=[], realtime=False, repeat=0):
        """Add an event to the queue"""
        event = Event(delay=delay, callback=callback, args=args,
                      realtime=realtime, repeat=repeat)
        insort_right(self._events, event)
    
    def tick(self):
        """Run all due events"""
        while self._events:
            event = self._events[0]
            if event.due < GLOBALS.game_time:
                if event.active:
                    event.callback(*event.args)
                    if event.repeat < 0:
                        self.add(delay=event.delay, callback=event.callback,
                                 args=event.args, realtime=event.realtime,
                                 repeat=event.repeat)
                    elif event.repeat > 1:
                        event.repeat -= 1
                        self.add(delay=event.delay, callback=event.callback,
                                 args=event.args, realtime=event.realtime,
                                 repeat=event.repeat)
                self._events.pop(0)
            else:
                # No more events are due
                break
