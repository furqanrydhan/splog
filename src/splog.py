#!/usr/bin/env python

import logging
import logging.handlers
import os.path
import sys

DEFAULT_LOGGER_SETTINGS = {
    'log':{
        'name':sys.argv[0] if len(sys.argv) > 0 else 'console',
        'level':'info',
        # File logging facility: if you configure an absolute directory and
        # relative filename (or absolute filename), we'll pipe log messages
        # there.
        'dir':None,
        'filename':None,
        # Port logging facility: if you do not configure filename and dir,
        # but do configure these, we'll pipe log messages to a Unix port.
        'address':None,
        'facility':None,
    },
}
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

class context_logger(logging.Logger):
    identifier = None
    def set_context(self, identifier):
        self.identifier = str(identifier) if identifier is not None else identifier
    def clear_context(self):
        self.identifier = None
    def _log(self, *args, **kwargs):
        msg = args[1]
        #msg = msg.replace('\n', ' ')
        if self.identifier is not None:
            try:
                msg = ' '.join([self.identifier, msg])
            except KeyboardInterrupt:
                raise
            except:
                try:
                    msg = ' '.join([self.identifier, unicode(msg)])
                except KeyboardInterrupt:
                    raise
                except:
                    msg = ' '.join([self.identifier, '(unencodable message)'])
        logging.Logger._log(self, *([args[0], msg] + list(args[2:])), **kwargs)

def configure(settings=DEFAULT_LOGGER_SETTINGS):
    if logging._splog_configured:
        warning('logging is being reconfigured')
    logging.setLoggerClass(context_logger)

    # create formatter
    formatter = logging.Formatter("            %(asctime)s %(name)s %(levelname)s %(message)s")
    logging._defaultFormatter = formatter

    name = settings.get('log', {}).get('name', None)
    filename = settings.get('log', {}).get('filename', None)
    if filename not in [None, ''] or settings.get('log', {}).get('dir', None) not in [None, '']:
        if filename in [None, '']:
            filename = name + '.log'
        if settings.get('log', {}).get('dir', None) not in [None, '']:
            filename = os.path.join(settings['log']['dir'], filename)
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(filename, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="UTF-8")
    elif settings.get('log', {}).get('address', None) not in [None, ''] and settings.get('log', {}).get('facility', None) not in [None, '']:
        handler = logging.handlers.SysLogHandler(address=settings['log']['address'], facility=settings['log']['facility'])
    else:
        # No filename given, use stdout
        handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler._splog_handler = True

    # Set up the root logger, otherwise the first call to generate log will do so and we'll get duplicate messages.
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        if hasattr(handler, '_splog_handler'):
            root_logger.removeHandler(handler)
    root_logger.setLevel(LEVELS.get(settings.get('log', {}).get('level', None), logging.NOTSET))
    root_logger.addHandler(handler)

    if logging._splog_configured:
        warning('logging has been reconfigured')
    else:
        logging._splog_configured = True

def logger(*args, **kwargs):
    if not logging._splog_configured:
        configure(*args, **kwargs)
    return logging.getLogger()

def log(level, line):
    logger().log(level, line)    

debug = lambda line: log(logging.DEBUG, line)
info = lambda line: log(logging.INFO, line)
warning = lambda line: log(logging.WARNING, line)
error = lambda line: log(logging.ERROR, line)
critical = lambda line: log(logging.CRITICAL, line)

def exception(line):
    logger().exception(line)

def set_context(identifier):
    return logger().set_context(identifier)
    
def clear_context():
    return logger().clear_context()
    
class context(object):
    def __init__(self, identifier):
        self._identifier = identifier
        self._old_identifier = None
    def __enter__(self):
        self._old_identifier = set_context(self._identifier)
    def __exit__(self, *args, **kwargs):
        set_context(self._old_identifier)
        self._identifer = None
        self._old_identifier = None