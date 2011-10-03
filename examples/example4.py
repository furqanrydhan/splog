#!/usr/bin/env python

KWARGS = {'host':'log.alcfd.com', 'facility':'local1', 'tag':'splog_example4'}

import splog
splog.configure(name='example4', **KWARGS)
splog.warning('Foo Bar')
