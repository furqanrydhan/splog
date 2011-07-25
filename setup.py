#!/usr/bin/env python
# -*- coding: utf-8 -*-

import distutils.core
 
def setup():
    distutils.core.setup(
        name='stylepage-log',
        version='0.1',
        description='StylePage tools: Python logging',
        author='mattbornski',
        url='http://github.com/mattbornski/splog',
        package_dir={'': 'src'},
        py_modules=[
            'splog',
        ],
    )

if __name__ == '__main__':
    setup()