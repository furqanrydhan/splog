#!/usr/bin/env python

import logging
import logging.handlers
import os.path
import sys

DEFAULT_LOGGER_SETTINGS = {
    'log':{
        'name':sys.argv[0] if len(sys.argv) > 0 else 'console',
        'level':'info',
    },
}
MAX_BYTES = 2097152000
BACKUP_COUNT = 1

_instance = None

class event_id_wrapper(logging.Logger):
    event_id = None
    def set_event(self, event_id):
        self.event_id = str(event_id) if event_id is not None else event_id
    def _log(self, *args, **kwargs):
        msg = args[1]
        #msg = msg.replace('\n', ' ')
        if self.event_id is not None:
            try:
                msg = ' '.join([self.event_id, msg])
            except KeyboardInterrupt:
                raise
            except:
                try:
                    msg = ' '.join([self.event_id, unicode(msg)])
                except KeyboardInterrupt:
                    raise
                except:
                    msg = ' '.join([self.event_id, '(unencodable message)'])
        logging.Logger._log(self, *([args[0], msg] + list(args[2:])), **kwargs)

def logger(name=None, settings=DEFAULT_LOGGER_SETTINGS):
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    logging.setLoggerClass(event_id_wrapper)

    # create formatter
    formatter = logging.Formatter("            %(asctime)s %(name)s %(levelname)s %(message)s")
    logging._defaultFormatter = formatter

    if name is None:
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

    # Set up the root logger, otherwise the first call to generate log will do so and we'll get duplicate messages.
    root_logger = logging.getLogger()
    root_logger.setLevel(levels.get(settings.get('log', {}).get('level', None), logging.NOTSET))
    root_logger.addHandler(handler)

    return logging.getLogger(name=name)

def configure(settings=DEFAULT_LOGGER_SETTINGS):
    global _instance
    _instance = logger(settings=settings)
    
def log(level, line):
    global _instance
    try:
        assert(_instance is not None)
    except AssertionError:
        configure()
    _instance.log(level, line)

debug = lambda line: log(logging.DEBUG, line)
info = lambda line: log(logging.INFO, line)
warning = lambda line: log(logging.WARNING, line)
error = lambda line: log(logging.ERROR, line)
critical = lambda line: log(logging.CRITICAL, line)