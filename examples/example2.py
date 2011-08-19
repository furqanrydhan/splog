#!/usr/bin/env python

import splog
splog.configure(filename='/tmp/foo.log')
splog.info('Foo Bar')
with open('/tmp/foo.log', 'r') as logfile:
    print logfile.read()