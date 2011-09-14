#!/usr/bin/env python

FILENAME = '/tmp/foo.log'

import os
import splog
splog.configure(filename=FILENAME)
splog.info('Foo Bar')
with open(FILENAME, 'r') as logfile:
    print logfile.read()
os.remove(FILENAME)