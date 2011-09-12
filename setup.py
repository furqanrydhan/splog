#!/usr/bin/env python
# -*- coding: utf-8 -*-

import distutils.core

__version__ = '0.1.4'

def setup():
    distutils.core.setup(
        name='splog',
        version=__version__,
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