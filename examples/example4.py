#!/usr/bin/env python

KWARGS = {'host':'log.alcfd.com', 'tag':'splog_example4'}

import splog
splog.configure(name='example4', **KWARGS)
splog.warning('Foo Bar')
