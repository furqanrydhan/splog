#!/usr/bin/env python

import logging
import logging.handlers
import os
import os.path
import pkg_resources
import sys
import time
import traceback

version = pkg_resources.require('splog')[0].version
__version__ = version

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
if not hasattr(logging, '_splog_name'):
    logging._splog_name = None

class context_logger(logging.Logger):
    _identifier = None
    def set_context(self, identifier):
        self._identifier = str(identifier) if identifier is not None else identifier
    def clear_context(self):
        self._identifier = None
    def _log(self, *args, **kwargs):
        line = unicode(args[1])
        if self._identifier is not None:
            line = ' '.join([self._identifier, line])
        logging.Logger._log(self, *([args[0], line] + list(args[2:])), **kwargs)

# Possible configuration arguments:
# name: the name that will be displayed in the log messages
# level: the minimum level of severity required to make it to the log
# dir:
# filename:
# address:
# facility: 
def configure(**kwargs):
    warnings = []
    if logging._splog_configured:
        warning('logging is being reconfigured')
        warnings.append('logging has been reconfigured')
        old_logger = logging.getLogger(logging._splog_name)
        for handler in old_logger.handlers[:]:
            old_logger.removeHandler(handler)
    logging.setLoggerClass(context_logger)

    # The handler controls where the log output goes
    logging._splog_name = kwargs.get('name', 'splog')
    filename = kwargs.get('filename', None)
    log_location = None
    if filename not in [None, ''] or kwargs.get('dir', None) not in [None, '']:
        if filename in [None, '']:
            filename = logging._splog_name + '.log'
        if kwargs.get('dir', None) not in [None, '']:
            filename = os.path.join(kwargs['dir'], filename)
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(filename, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="UTF-8")
        log_location = filename
    elif kwargs.get('address', None) not in [None, ''] and kwargs.get('facility', None) not in [None, '']:
        handler = logging.handlers.SysLogHandler(address=kwargs['address'], facility=kwargs['facility'])
        log_location = ':'.join([kwargs['address'], kwargs['facility']])
    else:
        # No filename given, use stdout
        handler = logging.StreamHandler(sys.stdout)
        log_location = 'stdout'
        
    # The formatter controls what the output looks like
    hostname = os.uname()[1]
    formatter = logging.Formatter(hostname + " %(asctime)s %(name)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)

    # The logger is the instance which will be returned when we call getLogger()
    logger = logging.getLogger(logging._splog_name)
    logger.propagate = 0
    try:
        logger.setLevel(LEVELS[kwargs.get('level', 'info')])
    except KeyError:
        logger.setLevel(LEVELS['info'])
        warnings.append('logging level not valid: ' + str(kwargs['level']))
    logger.addHandler(handler)

    logging._splog_configured = True
    for w in warnings:
        warning(w)
    info('logging to ' + log_location)
    if log_location not in ['stdout']:
        print 'logging to ' + log_location

def logger(**kwargs):
    if not logging._splog_configured:
        configure(**kwargs)
    return logging.getLogger(logging._splog_name)

debug = lambda msg: logger().debug(msg)
info = lambda msg: logger().info(msg)
warning = lambda msg: logger().warning(msg)
error = lambda msg: logger().error(msg)
critical = lambda msg: logger().critical(msg)

def exception(e):
    for line in traceback.format_exc().splitlines():
        logger().error(line)

def set_context(identifier):
    return logger().set_context(identifier)
    
def clear_context():
    return logger().clear_context()
    
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
        self._identifer = None
        self._old_identifier = None
