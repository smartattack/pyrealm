"""
Logging module
"""

class Logger():
    def __init__(self, filename):
        _logfile = filename
        _log = open(_logfile, 'a', 0)

    def add(self, msg):
        _log.write(msg)

