#!/usr/bin/env python

import splog
splog.configure(address='/dev/log', facility='local1')
splog.info('Foo Bar')