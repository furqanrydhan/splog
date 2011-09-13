#!/usr/bin/env python
# -*- coding: utf-8 -*-

import distutils.core

def setup():
    with open('src/_version.py', 'r') as f:
        for line in f.readlines():
            if 'version' in line:
                try:
                    exec(line)
                except SyntaxError:
                    pass
    try:
        assert(isinstance(version, basestring))
    except AssertionError:
        version = 'unknown'
    distutils.core.setup(
        name='splog',
        version=version,
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