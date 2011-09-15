#!/usr/bin/env python

KWARGS = {'address':'/dev/log', 'facility':'local1'}

import logging
import logging.handlers
logging.getLogger().addHandler(logging.handlers.SysLogHandler(**KWARGS))
logging.getLogger().warning('Bar Foo')

import splog
splog.configure(name='example4', **KWARGS)
splog.warning('Foo Bar')
