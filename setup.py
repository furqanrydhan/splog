#!/usr/bin/env python
# -*- coding: utf-8 -*-

import distutils.core
 
def setup():
    distutils.core.setup(
        name='splog',
        version='0.1.1',
        description='StylePage tools: Python logging',
        author='mattbornski',
        url='http://github.com/stylepage/splog',
        package_dir={'': 'src'},
        py_modules=[
            'splog',
        ],
    )

if __name__ == '__main__':
    setup()