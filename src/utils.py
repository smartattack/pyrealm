"""
Utility functions for PyRealm

Logging, text manipulation, colorization.
"""

import logging
import time


def init_log(filename='log/pyrealm.log', level=logging.DEBUG):
    """Called only once in main to give us consistent logging"""
    log = logging.getLogger('self.log')
    log.setLevel(level)
    file = logging.FileHandler(filename)
    if level == logging.DEBUG:
        file.setFormatter(logging.Formatter(
            '%(asctime)s %(filename)s:%(lineno)s %(levelname)s: %(message)s'))
    else:
        file.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'))
    log.addHandler(file)
    return log


# I will be global
log = init_log()


def time_to_string(timeobj):
    """Convert a time object to a string"""
    return time.ctime(int(timeobj))


def stat_color(current: int, maximum: int):
    """Provide color code based on stat % of max"""
    # Get ratio, avoid divide by zero
    stat_ratio = float(current / (maximum + .0001))
    if stat_ratio < 0.25:
        return '^R'
    elif stat_ratio < 0.5:
        return '^Y'
    else:
        return '^G'


def calc_xp(level):
    """Return XP for a given level"""
    log.debug('FUNC calc_xp()')
    # Some coefficients: 150 -2 200,   100 -2 200
    a, b, c = 10, -2, 200
    return int((a * level) ** 2 + b * level + c)


def xp_to_level(current_level, current_xp):
    """Find XP needed to reach the next level"""
    log.debug('FUNC xp_to_level()')
    return calc_xp(current_level+1) - current_xp


def wrap_one_line(input, width):
    """Returns a one line wrapped to width
    and the return of the text as a tuple (first_line, remaining)"""
    words = input.split()
    first_line = ''
    while words:
        try:
            word = words.pop(0)
        except Exception as err:
            log.debug("Uh oh: %s", err)
        if len(first_line + ' ' + word) > width:
            return (first_line.lstrip(), word + ' ' + ' '.join(words))
        else:
            first_line += ' ' + word
    return (first_line.lstrip(), None)
