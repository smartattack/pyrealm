"""
Helpful debug utils
"""

import resource
import gc
import objgraph
from utils import log

def log_usage():
    """Log some usage information - call me from scheduler"""
    output = 'Usage statistics: {}'.format(resource.getrusage(resource.RUSAGE_SELF))
    log.debug(output)


def log_objgraph():
    """Log memory usage breakdown by objects"""
    gc.collect()
    log.debug(objgraph.show_most_common_types())


"""
0	ru_utime	time in user mode (float)
1	ru_stime	time in system mode (float)
2	ru_maxrss	maximum resident set size
3	ru_ixrss	shared memory size
4	ru_idrss	unshared memory size
5	ru_isrss	unshared stack size
6	ru_minflt	page faults not requiring I/O
7	ru_majflt	page faults requiring I/O
8	ru_nswap	number of swap outs
9	ru_inblock	block input operations
10	ru_oublock	block output operations
11	ru_msgsnd	messages sent
12	ru_msgrcv	messages received
13	ru_nsignals	signals received
14	ru_nvcsw	voluntary context switches
15	ru_nivcsw	involuntary context switches
"""