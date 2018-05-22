import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from colorlog import ColoredFormatter


# Default logging facilities
LOG_LEVEL = logging.INFO
LOGFORMAT = ("  %(log_color)s%(levelname)-8s%(reset)s |"
             " %(log_color)s%(message)s%(reset)s")
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)

log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

log2 = logging.getLogger("bookied_sync")
log2.setLevel(LOG_LEVEL)

for l in [log, log2]:
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    l.addHandler(stream)
