import signal
import gevent

# in case zombie
gevent.signal(signal.SIGQUIT, gevent.kill)

from gevent.monkey import *
