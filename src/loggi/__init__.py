import logging
from logging import Logger

from .logger import getLogger, load_log, get_logpaths, get_logpath, get_log
from .models import Log, Event

__version__ = "0.1.1"

CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET
