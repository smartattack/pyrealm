"""
Helpful debug utils
"""

import resource
import time
import gc
import objgraph
from utils import log
import globals as GLOBALS

def log_snapshot(data):
    """Log some usage information - call me from scheduler"""
    output = 'Resource snapshot:  {}'.format(data)
    log.debug(output)


def take_resource_snapshot():
    """Return a snapshot of resource usage"""
    return (time.time(), resource.getrusage(resource.RUSAGE_SELF))


def snapshot_delta(current, last):
    """Return a diff between this snapshot versus another snapshot"""
    output = 'Resource changes in the past {} seconds:\n'.format(int(current[0] - last[0]))
    for name, desc in [
        ('ru_utime', 'time in user mode (float)'),
        ('ru_stime', 'time in system mode (float)'),
        ('ru_maxrss', 'maximum resident set size'),
        ('ru_ixrss', 'shared memory size'),
        ('ru_idrss', 'unshared memory size'),
        ('ru_isrss', 'unshared stack size'),
        ('ru_minflt', 'page faults not requiring I/O'),
        ('ru_majflt', 'page faults requiring I/O'),
        ('ru_nswap', 'number of swap outs'),
        ('ru_inblock', 'block input operations'),
        ('ru_oublock', 'block output operations'),
        ('ru_msgsnd', 'messages sent'),
        ('ru_msgrcv', 'messages received'),
        ('ru_nsignals', 'signals received'),
        ('ru_nvcsw', 'voluntary context switches'),
        ('ru_nivcsw', 'involuntary context switches')]:
        cdata = getattr(current[1], name)
        ldata = getattr(last[1], name)
        delta = cdata - ldata
        output += '{:30s} = {:14.5f}, Delta = {:14.5f}\n'.format(desc, cdata, delta)
    return output


def update_snapshot():
    """Take a snapshot, diff from last"""
    GLOBALS.current_snapshot = take_resource_snapshot()
    if GLOBALS.last_snapshot:
        delta = snapshot_delta(GLOBALS.current_snapshot, GLOBALS.last_snapshot)
        log_snapshot(delta)
    else:
        # First snapshot has no delta
        log_snapshot(GLOBALS.current_snapshot)
    GLOBALS.last_snapshot = GLOBALS.current_snapshot


def log_objgraph():
    """Log memory usage breakdown by objects"""
    gc.collect()
    log.debug(objgraph.show_most_common_types())


"""
[
(0, 'ru_utime', 'time in user mode (float)'),
(1, 'ru_stime', 'time in system mode (float)'),
(2, 'ru_maxrss', 'maximum resident set size'),
(3, 'ru_ixrss', 'shared memory size'),
(4, 'ru_idrss', 'unshared memory size'),
(5, 'ru_isrss', 'unshared stack size'),
(6, 'ru_minflt', 'page faults not requiring I/O'),
(7, 'ru_majflt', 'page faults requiring I/O'),
(8, 'ru_nswap', 'number of swap outs'),
(9, 'ru_inblock', 'block input operations'),
(10, 'ru_oublock', 'block output operations'),
(11, 'ru_msgsnd', 'messages sent'),
(12, 'ru_msgrcv', 'messages received'),
(13, 'ru_nsignals', 'signals received'),
(14, 'ru_nvcsw', 'voluntary context switches'),
(15, 'ru_nivcsw', 'involuntary context switches')
]
"""