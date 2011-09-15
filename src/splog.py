#!/usr/bin/env python

__version_info__ = (0, 1, 8)
__version__ = '.'.join([str(i) for i in __version_info__])
version = __version__

import logging
import logging.handlers
import os
import os.path
import sys
import time
import traceback

MAX_BYTES = 2097152000
BACKUP_COUNT = 1
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

if not hasattr(logging, '_splog_configured'):
    logging._splog_configured = False
    logging._splog_root_logger = None
    logging._splog_handler = None
    logging._splog_hostname = None
    logging._splog_logger_name = None
    logging._splog_context_identifier = None

# Possible configuration arguments:
# name: the name that will be displayed in the log messages
# level: the minimum level of severity required to make it to the log
# dir:
# filename:
# address:
# facility: 
def configure(**kwargs):
    warnings = []
    logging._splog_root_logger = logging.getLogger()
    if logging._splog_configured:
        warning('logging is being reconfigured')
        warnings.append('logging has been reconfigured')
        logging._splog_root_logger.removeHandler(logging._splog_handler)

    # The handler controls where the log output goes
    filename = None
    try:
        assert(kwargs['filename'] not in ['', None])
        filename = kwargs['filename']
    except (AssertionError, KeyError):
        try:
            assert(kwargs['dir'] not in [None, ''])
            assert(kwargs['name'] not in [None, ''])
            filename = os.path.join(kwargs['dir'], kwargs['name'] + '.log')
        except (AssertionError, KeyError):
            filename = None
    log_location = None
    if filename is not None:
        # Add the log message handler to the logger
        logging._splog_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="UTF-8")
        log_location = filename
    elif kwargs.get('address', None) not in [None, ''] and kwargs.get('facility', None) not in [None, '']:
        logging._splog_handler = logging.handlers.SysLogHandler(address=kwargs['address'], facility=kwargs['facility'])
        log_location = ':'.join([kwargs['address'], kwargs['facility']])
    else:
        # No filename given, use stdout
        logging._splog_handler = logging.StreamHandler(sys.stdout)
        log_location = 'stdout'
        
    # The formatter controls what the output looks like
    logging._splog_hostname = str(os.uname()[1])
    name = kwargs.get('name', None)
    if name in [None, '']:
        name = 'root'
    logging._splog_logger_name = str(name)

    try:
        logging._splog_root_logger.setLevel(LEVELS[kwargs.get('level', 'info')])
    except KeyError:
        logging._splog_root_logger.setLevel(LEVELS['info'])
        warnings.append('logging level not valid: ' + str(kwargs['level']))
    logging._splog_root_logger.addHandler(logging._splog_handler)

    # Wrap the root logger
    logging._splog_configured = True
    clear_context()
    for w in warnings:
        warning(w)
    info('logging to ' + log_location)
    if log_location not in ['stdout']:
        print 'logging to ' + log_location

def logger(**kwargs):
    if not logging._splog_configured:
        configure(**kwargs)
    return logging._splog_root_logger

debug = lambda msg: logger().debug(msg)
info = lambda msg: logger().info(msg)
warning = lambda msg: logger().warning(msg)
error = lambda msg: logger().error(msg)
critical = lambda msg: logger().critical(msg)

def exception(msg):
    logger().error(msg)
    for line in traceback.format_exc().splitlines():
        logger().error(line)

def set_context(identifier):
    if not logging._splog_configured:
        configure()
    ret = logging._splog_context_identifier
    logging._splog_context_identifier = str(identifier) if identifier is not None else None
    formatter = logging.Formatter(' '.join([logging._splog_hostname, '%(asctime)s', logging._splog_logger_name, '%(levelname)s'] + ([logging._splog_context_identifier] if logging._splog_context_identifier is not None else []) + ['%(message)s']))
    logging._splog_handler.setFormatter(formatter)
    return ret
    
def clear_context():
    set_context(None)

class context(object):
    def __init__(self, identifier):
        self._identifier = identifier
        self._old_identifier = None
        self._start_time = None
    def __enter__(self):
        self._old_identifier = set_context(str(self._identifier))
        self._start_time = time.time()
        info('+++ ' + str(self._identifier) + ' +++')
    def __exit__(self, *args, **kwargs):
        info(str(time.time() - self._start_time) + ' seconds elapsed')
        info('--- ' + str(self._identifier) + ' ---')
        set_context(self._old_identifier)
        self._identifier = None
        self._old_identifier = None
